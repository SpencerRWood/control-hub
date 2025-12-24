// src/features/approvals/listUtils.ts
import type { ApprovalItem, ApprovalStatus } from "./types";

export function matchesQuery(a: ApprovalItem, q: string) {
  if (!q) return true;
  const needle = q.trim().toLowerCase();
  if (!needle) return true;

  return (
    String(a.id).includes(needle) ||
    a.title.toLowerCase().includes(needle) ||
    a.requested_by.toLowerCase().includes(needle)
  );
}

export function filterApprovals(items: ApprovalItem[], status: ApprovalStatus | "ALL", q: string) {
  return items.filter((a) => (status === "ALL" ? true : a.status === status)).filter((a) => matchesQuery(a, q));
}

export function paginate<T>(items: T[], page: number, pageSize: number) {
  const total = items.length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * pageSize;
  return {
    page: safePage,
    pageSize,
    total,
    totalPages,
    slice: items.slice(start, start + pageSize),
  };
}
