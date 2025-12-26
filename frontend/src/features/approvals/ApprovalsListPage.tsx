// src/features/approvals/ApprovalsListPage.tsx
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useApprovalsList, useDecideApproval } from "./queries";
import type { ApprovalStatus } from "./types";
import { filterApprovals, paginate } from "./listUtils";
import { ApprovalsTable } from "@/features/approvals/ApprovalsTable";
import { toast } from "sonner";

function useDebounced<T>(value: T, ms = 300) {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return v;
}

function getInt(sp: URLSearchParams, key: string, fallback: number) {
  const n = Number(sp.get(key) ?? fallback);
  return Number.isFinite(n) ? n : fallback;
}

export function ApprovalsListPage() {
  const [sp, setSp] = useSearchParams();
  const status = (sp.get("status") ?? "ALL") as ApprovalStatus | "ALL";
  const page = Math.max(1, getInt(sp, "page", 1));
  const pageSize = Math.min(100, Math.max(5, getInt(sp, "page_size", 10)));
  const qParam = sp.get("q") ?? "";

  const [search, setSearch] = useState(qParam);
  const debounced = useDebounced(search, 300);

  useEffect(() => setSearch(qParam), [qParam]);

  useEffect(() => {
    if (debounced === qParam) return;
    const n = new URLSearchParams(sp);
    debounced ? n.set("q", debounced) : n.delete("q");
    n.set("page", "1");
    setSp(n, { replace: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debounced]);

  const listQ = useApprovalsList();
  const decide = useDecideApproval();

  const filtered = useMemo(
    () => filterApprovals(listQ.data ?? [], status, qParam),
    [listQ.data, status, qParam]
  );

  const paged = useMemo(() => paginate(filtered, page, pageSize), [filtered, page, pageSize]);

  const setParams = (next: Partial<{ status: ApprovalStatus | "ALL"; page: number; page_size: number; q: string }>) => {
    const n = new URLSearchParams(sp);
    if (next.status !== undefined) n.set("status", next.status);
    if (next.page !== undefined) n.set("page", String(next.page));
    if (next.page_size !== undefined) n.set("page_size", String(next.page_size));
    if (next.q !== undefined) (next.q ? n.set("q", next.q) : n.delete("q"));
    setSp(n, { replace: true });
  };

  const onApprove = (id: number, decision_reason?: string) => {
    decide.mutate(
      { id, action: "approve", decision_reason: decision_reason ?? null },
      {
        onSuccess: () => toast({ title: "Approved" }),
        onError: (e: any) =>
          toast({
            title: "Approve failed",
            description: e?.message ?? "Unknown error",
            variant: "destructive",
          }),
      }
    );
  };

  const onReject = (id: number, decision_reason?: string) => {
    decide.mutate(
      { id, action: "reject", decision_reason: decision_reason ?? null },
      {
        onSuccess: () => toast({ title: "Rejected" }),
        onError: (e: any) =>
          toast({
            title: "Reject failed",
            description: e?.message ?? "Unknown error",
            variant: "destructive",
          }),
      }
    );
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-2">
          <div className="w-[200px]">
            <Select value={status} onValueChange={(v) => setParams({ status: v as any, page: 1 })}>
              <SelectTrigger>
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All</SelectItem>
                <SelectItem value="PENDING">Pending</SelectItem>
                <SelectItem value="APPROVED">Approved</SelectItem>
                <SelectItem value="REJECTED">Rejected</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Input
            className="w-[320px]"
            placeholder="Search by title, requester, or id…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <Button
          variant="outline"
          onClick={() => setSp(new URLSearchParams({ status: "ALL", page: "1", page_size: "10" }), { replace: true })}
        >
          Reset
        </Button>
      </div>

      {listQ.isLoading ? (
        <div className="text-sm text-muted-foreground">Loading…</div>
      ) : listQ.isError ? (
        <div className="text-sm text-destructive">Failed to load approvals.</div>
      ) : (
        <ApprovalsTable
          rows={paged.slice}
          page={paged.page}
          pageSize={paged.pageSize}
          total={paged.total}
          onPrev={() => setParams({ page: paged.page - 1 })}
          onNext={() => setParams({ page: paged.page + 1 })}
          onPageSizeChange={(n) => setParams({ page_size: n, page: 1 })}
          onApprove={onApprove}
          onReject={onReject}
          isDeciding={decide.isPending}
        />
      )}
    </div>
  );
}
