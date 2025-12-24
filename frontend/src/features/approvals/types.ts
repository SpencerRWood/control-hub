// src/features/approvals/types.ts
export type ApprovalStatus = "PENDING" | "APPROVED" | "REJECTED";

export type ApprovalItem = {
  id: number;
  title: string;
  description: string;
  type: string;
  payload_json: unknown;
  status: ApprovalStatus;
  requested_by: string;
  assigned_to: string;
  created_at: string;
  updated_at: string;
  decision_at: string | null;
  decision_by: string | null;
  decision_reason: string | null;
};
