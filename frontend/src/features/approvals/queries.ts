import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { ApprovalItem } from "./types";

export function useApprovalItem(id?: string) {
  return useQuery({
    queryKey: ["approvals", id],
    enabled: !!id,
    queryFn: async () => {
      const res = await api.get<ApprovalItem>(`/approvals/${id}`);
      return res.data;
    },
  });
}
