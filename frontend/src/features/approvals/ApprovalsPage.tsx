import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export function ApprovalsPage() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <div className="text-xl font-semibold">Approvals</div>
        <Badge variant="secondary">UI Shell</Badge>
      </div>

      <Button onClick={() => toast("Ready", { description: "Next: approvals list." })}>
        Continue
      </Button>
    </div>
  );
}