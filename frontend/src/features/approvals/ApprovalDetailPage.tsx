import { useParams, Link, Navigate } from "react-router-dom";
import { useApprovalItem } from "./queries";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function ApprovalDetailPage() {
  const { id } = useParams();
  const q = useApprovalItem(id);

  if (!id) return <Navigate to="/approvals" replace />;
  if (q.isLoading) return <div className="text-sm text-muted-foreground">Loading…</div>;

  if (q.isError || !q.data) {
    return (
      <div className="space-y-4">
        <div className="text-xl font-semibold">Approval not found</div>
        <Button asChild variant="outline">
          <Link to="/approvals">Back to approvals</Link>
        </Button>
      </div>
    );
  }

  const a = q.data;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="text-xl font-semibold">Approval #{a.id}</div>
        <Badge variant="outline">{a.status}</Badge>
        <Badge variant="secondary">{a.type}</Badge>
      </div>

      <pre className="max-h-[70vh] overflow-auto rounded-md bg-muted p-4 text-xs">
        {JSON.stringify(a, null, 2)}
      </pre>

      <Button asChild variant="outline">
        <Link to="/approvals">Back</Link>
      </Button>
    </div>
  );
}
