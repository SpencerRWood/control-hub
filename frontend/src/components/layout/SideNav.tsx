import { NavLink } from "react-router-dom";
import { Separator } from "@/components/ui/separator";

const linkBase =
  "flex items-center rounded-md px-3 py-2 text-sm transition-colors";
const linkActive = "bg-muted text-foreground";
const linkIdle = "text-muted-foreground hover:bg-muted hover:text-foreground";

export function SideNav() {
  return (
    <div className="flex h-full flex-col p-4">
      <div className="px-2 py-2">
        <div className="text-lg font-semibold leading-none">Control Hub</div>
        <div className="mt-1 text-xs text-muted-foreground">Approvals dashboard</div>
      </div>

      <Separator className="my-4" />

      <nav className="space-y-1">
        <NavLink
          to="/approvals"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? linkActive : linkIdle}`
          }
          end
        >
          Approvals
        </NavLink>
        <NavLink
        to="/chat"
        className={({ isActive }) => `${linkBase} ${isActive ? linkActive : linkIdle}`}
      >
        Chat
      </NavLink>
      </nav>

      <div className="mt-auto px-2 pt-6 text-xs text-muted-foreground">
        v0.1
      </div>
    </div>
  );
}
