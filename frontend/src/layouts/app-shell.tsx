import type { PropsWithChildren } from "react";
import { Button } from "@/components/ui/button";

const sections = [
  { id: "about", label: "About" },
  { id: "services", label: "Services" },
  { id: "why-us", label: "Why Us" },
  { id: "contact", label: "Contact" },
];

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-svh flex flex-col bg-background text-foreground">
      <header className="border-b bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3 md:px-6">
          <span className="text-base font-semibold tracking-tight">
            Wood Analytics
          </span>

          <nav className="hidden gap-6 text-sm font-medium md:flex">
            {sections.map((section) => (
              <button
                key={section.id}
                className="text-muted-foreground hover:text-foreground transition-colors"
                onClick={() => {
                  const el = document.getElementById(section.id);
                  el?.scrollIntoView({ behavior: "smooth" });
                }}
              >
                {section.label}
              </button>
            ))}
          </nav>

          <Button
            size="sm"
            className="ml-4"
            onClick={() => {
              const el = document.getElementById("contact");
              el?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            Get Started
          </Button>
        </div>
      </header>

      <main className="flex-1">
        <div className="mx-auto max-w-5xl px-4 py-10 md:px-6 md:py-16">
          {children}
        </div>
      </main>

      <footer className="border-t">
        <div className="mx-auto flex max-w-5xl flex-col gap-2 px-4 py-6 text-xs text-muted-foreground md:flex-row md:items-center md:justify-between md:px-6">
          <span>© {new Date().getFullYear()} Wood Analytics.</span>
          <div className="flex gap-4">
            <a href="#about" className="hover:text-foreground">
              About
            </a>
            <a href="#services" className="hover:text-foreground">
              Services
            </a>
            <a href="#why-us" className="hover:text-foreground">
              Why Us
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
