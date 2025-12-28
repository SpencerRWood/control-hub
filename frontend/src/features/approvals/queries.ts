// src/features/approvals/queries.ts
import { useMutation, useQuery } from "@tanstack/react-query";
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

type DecideAction = "approve" | "reject";

type DecideInput = {
  id: number;
  action: DecideAction;
  decision_reason?: string | null;
  decision_by?: string; // allow override if you want
};

export function useDecideApproval() {
  return useMutation({
    mutationFn: async ({ id, action, decision_reason, decision_by }: DecideInput) => {
      const body: { decision_by: string; decision_reason?: string } = {
        // TODO: replace with actual user identity
        decision_by: decision_by ?? "user:spencer",
      };

      if (decision_reason && decision_reason.trim().length > 0) {
        body.decision_reason = decision_reason.trim();
      }

      // Enforce backend requirement for reject
      if (action === "reject" && !body.decision_reason) {
        throw new Error("Rejection requires a decision reason.");
      }

      const res = await api.post(`/approvals/${id}/${action}`, body);
      return res.data;
    },
  });
}

