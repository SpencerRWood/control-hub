// src/features/approvals/ApprovalsTable.tsx
import { Link } from "react-router-dom";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { ApprovalItem } from "./types";

type ApprovalsTableProps = {
  rows: ApprovalItem[];
  page: number;
  pageSize: number;
  total: number;
  onPrev: () => void;
  onNext: () => void;
  onPageSizeChange: (n: number) => void;
  onApprove: (id: number, decision_reason?: string) => void;
  onReject: (id: number, decision_reason?: string) => void;
  isDeciding?: boolean;
  decidingId?: number | null;
};

export function ApprovalsTable(props: ApprovalsTableProps) {
  const {
    rows,
    page,
    pageSize,
    total,
    onPrev,
    onNext,
    onPageSizeChange,
    onApprove,
    onReject,
    isDeciding = false,
    decidingId = null,
  } = props;

  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const canPrev = page > 1;
  const canNext = page < totalPages;

  return (
    <div className="space-y-3">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Title</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Requested By</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {rows.map((a) => {
            const isPending = a.status === "PENDING";
            const isThisRowDeciding = decidingId === a.id;
            const disabled = !isPending || isThisRowDeciding || isDeciding;

            return (
              <TableRow key={a.id}>
                <TableCell className="font-mono text-xs">{a.id}</TableCell>

                <TableCell>
                  <Link to={`/approvals/${a.id}`} className="underline underline-offset-4">
                    {a.title}
                  </Link>
                  <div className="text-xs text-muted-foreground">{a.type}</div>
                </TableCell>

                <TableCell>
                  <Badge
                    variant={
                      a.status === "PENDING"
                        ? "secondary"
                        : a.status === "APPROVED"
                        ? "default"
                        : "destructive"
                    }
                  >
                    {a.status}
                  </Badge>
                </TableCell>

                <TableCell className="text-sm">{a.requested_by}</TableCell>

                <TableCell className="text-right space-x-2">
                <Button
                  size="sm"
                  disabled={disabled}
                  onClick={() => onApprove(a.id)}
                >
                  Approve
                </Button>

                <Button
                  size="sm"
                  variant="destructive"
                  disabled={disabled}
                  onClick={() => {
                    const reason = window.prompt("Reason for rejection?");
                    if (reason === null) return; // user cancelled
                    onReject(a.id, reason);
                  }}
                >
                  Reject
                </Button>
                </TableCell>
              </TableRow>
            );
          })}

          {rows.length === 0 && (
            <TableRow>
              <TableCell colSpan={5} className="text-sm text-muted-foreground">
                No approvals found.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>

      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          Page {page} of {totalPages} • {total} total
        </div>

        <div className="flex items-center gap-2">
          <select
            className="h-9 rounded-md border bg-background px-2 text-sm"
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
          >
            {[10, 25, 50].map((n) => (
              <option key={n} value={n}>
                {n} / page
              </option>
            ))}
          </select>

          <Button variant="outline" size="sm" onClick={onPrev} disabled={!canPrev}>
            Prev
          </Button>
          <Button variant="outline" size="sm" onClick={onNext} disabled={!canNext}>
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
