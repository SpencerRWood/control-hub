import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export function TopBar() {
  return (
    <div className="flex h-14 items-center gap-3 px-6">
      <div className="text-sm font-medium">Approvals</div>

      <div className="ml-auto flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => toast("Pong", { description: "UI shell is wired up." })}
        >
          Test toast
        </Button>
      </div>
    </div>
  );
}
