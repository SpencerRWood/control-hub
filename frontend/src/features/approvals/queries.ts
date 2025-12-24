// src/features/approvals/queries.ts
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { ApprovalItem } from "./types";

export function useApprovalItem(id?: string) {
  return useQuery({
    queryKey: ["approvals", "item", id],
    enabled: !!id,
    queryFn: async () => {
      const res = await api.get<ApprovalItem>(`/approvals/${id}`);
      return res.data;
    },
  });
}

export function useApprovalsList() {
  return useQuery({
    queryKey: ["approvals", "list"],
    queryFn: async () => {
      const res = await api.get<ApprovalItem[]>("/approvals");
      return res.data;
    },
    staleTime: 10_000,
  });
}

export type DecideAction = "approve" | "reject";

export type DecideApprovalInput = {
  id: number;
  action: DecideAction;
  // optional comment; include only if your backend accepts a body
  decision_reason?: string | null;
};

export function useDecideApproval() {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, action, decision_reason }: DecideApprovalInput) => {
      // If backend expects no body, set second arg to undefined.
      const res = await api.post<ApprovalItem>(
        `/approvals/${id}/${action}`,
        decision_reason?.trim() ? { decision_reason: decision_reason.trim() } : undefined
      );
      return res.data;
    },
    onSuccess: (updated) => {
      qc.setQueryData(["approvals", "item", String(updated.id)], updated);
      qc.setQueryData<ApprovalItem[]>(["approvals", "list"], (prev) =>
        prev ? prev.map((a) => (a.id === updated.id ? updated : a)) : prev
      );
      qc.invalidateQueries({ queryKey: ["approvals"] });
    },
  });
}
