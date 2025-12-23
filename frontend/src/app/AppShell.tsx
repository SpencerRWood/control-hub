import { Outlet } from "react-router-dom";
import { SideNav } from "@/components/layout/SideNav";
import { TopBar } from "@/components/layout/TopBar";

export function AppShell() {
  return (
    <div className="min-h-screen bg-background">
      <div className="grid min-h-screen grid-cols-[260px_1fr]">
        <aside className="border-r">
          <SideNav />
        </aside>

        <div className="flex min-w-0 flex-col">
          <header className="border-b">
            <TopBar />
          </header>

          <main className="min-w-0 p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
