// src/features/chat/ChatPage.tsx
import * as React from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";
import { ChevronDown, Plus, UserPlus, SendHorizonal } from "lucide-react";
import { useChatThread, useCreateChatThread, usePostChatMessage } from "./queries";
import type { ChatMessage } from "./types";

const STORAGE_KEY = "controlhub.chat.thread_id";

function isUser(m: ChatMessage) {
  return m.role === "user";
}

export function ChatPage() {
  const [threadId, setThreadId] = React.useState<string | null>(() =>
    localStorage.getItem(STORAGE_KEY)
  );
  const [input, setInput] = React.useState("");

  // ✅ NEW: purely-UI state so we can "expand" only after first send,
  // regardless of whether the backend thread fetch has refreshed yet.
  const [hasStarted, setHasStarted] = React.useState(false);

  const createThread = useCreateChatThread();
  const threadQ = useChatThread(threadId ?? undefined);
  const postMsg = usePostChatMessage(threadId ?? "__unset__");

  const messages = threadQ.data?.messages ?? [];

  // prevent runaway loop
  const didInit = React.useRef(false);

  // auto-scroll for expanded view
  const bottomRef = React.useRef<HTMLDivElement | null>(null);

  React.useEffect(() => {
    if (didInit.current) return;
    didInit.current = true;

    if (threadId) return;

    createThread.mutate(
      { created_by: "user:spencer", title: "Chat", metadata_json: { source: "ui" } },
      {
        onSuccess: (t) => {
          localStorage.setItem(STORAGE_KEY, t.thread_id);
          setThreadId(t.thread_id);
        },
      }
    );

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [threadId]);

  // If backend already has messages (e.g., reload), start expanded
  React.useEffect(() => {
    if (messages.length > 0) setHasStarted(true);
  }, [messages.length]);

  React.useEffect(() => {
    if (!hasStarted) return;
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [hasStarted, messages.length]);

  function onSend() {
    if (!threadId) return;
    const content = input.trim();
    if (!content || postMsg.isPending) return;

    // ✅ Expand immediately on first send (before network returns)
    if (!hasStarted) setHasStarted(true);

    setInput("");
    postMsg.mutate({
      content,
      use_rag: false,
      max_citations: 0,
      metadata_json: { client: "frontend" },
    });
  }

  const canSend = !!threadId && !!input.trim() && !postMsg.isPending && !createThread.isPending;

  // "Landing" view is only when the UI hasn't started yet (even if messages are empty)
  const showLanding = !hasStarted;

  function resetThread() {
    localStorage.removeItem(STORAGE_KEY);
    setThreadId(null);
    setInput("");
    setHasStarted(false);
    didInit.current = false;
  }

  return (
    <div className="h-full min-h-full w-full bg-background text-foreground">
      {/* Top row */}
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-9 gap-2 px-2 text-sm">
              <span className="font-medium">ChatGPT 5.2</span>
              <ChevronDown className="h-4 w-4 opacity-70" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="w-56">
            <DropdownMenuItem>ChatGPT 5.2</DropdownMenuItem>
            <DropdownMenuItem disabled>More models…</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" className="h-9 w-9" onClick={resetThread}>
            <Plus className="h-4 w-4 opacity-80" />
          </Button>
          <Button variant="ghost" size="icon" className="h-9 w-9">
            <UserPlus className="h-4 w-4 opacity-80" />
          </Button>
          <Button variant="ghost" size="icon" className="h-9 w-9" aria-label="Placeholder">
            <div className="h-4 w-4 rounded-full border border-foreground/40" />
          </Button>
        </div>
      </div>

      {/* Main */}
      <div className="mx-auto flex h-[calc(100%-4.25rem)] max-w-5xl flex-col px-4 pb-6 pt-16">
        {showLanding ? (
          <div className="flex flex-1 flex-col items-center justify-center">
            <div className="mb-6 text-center text-3xl font-medium tracking-tight">
              Where should we begin?
            </div>

            <ComposerPill
              value={input}
              onChange={setInput}
              onSend={onSend}
              disabled={postMsg.isPending}
              canSend={canSend}
            />
          </div>
        ) : (
          <div className="mx-auto flex h-full w-full max-w-3xl flex-col">
            <div className="flex-1 overflow-y-auto py-6">
              <div className="space-y-6">
                {messages.map((m) => (
                  <div
                    key={m.message_id}
                    className={cn("flex", isUser(m) ? "justify-end" : "justify-start")}
                  >
                    <div
                      className={cn(
                        "max-w-[85%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-relaxed",
                        isUser(m)
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted/40 border border-border"
                      )}
                    >
                      {m.content}
                    </div>
                  </div>
                ))}

                <div ref={bottomRef} />
              </div>
            </div>

            <div className="pt-2">
              <ComposerPill
                value={input}
                onChange={setInput}
                onSend={onSend}
                disabled={postMsg.isPending}
                canSend={canSend}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function ComposerPill(props: {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  disabled: boolean;
  canSend: boolean;
}) {
  const { value, onChange, onSend, disabled, canSend } = props;

  return (
    <div className="w-full max-w-[720px]">
      <div className="flex items-center gap-2 rounded-full border border-border bg-muted/30 px-3 py-2 shadow-sm">
        <Button variant="ghost" size="icon" className="h-10 w-10 rounded-full">
          <Plus className="h-4 w-4 opacity-80" />
        </Button>

        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Ask anything"
          className={cn(
            "min-h-[44px] flex-1 resize-none border-0 bg-transparent px-2 py-2 text-sm",
            "focus-visible:ring-0 focus-visible:ring-offset-0"
          )}
          rows={1}
          disabled={disabled}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
              e.preventDefault();
              onSend();
            }
          }}
        />

        <Button
          size="icon"
          className="h-10 w-10 rounded-full"
          onClick={onSend}
          disabled={!canSend}
          aria-label="Send"
        >
          <SendHorizonal className="h-4 w-4" />
        </Button>
      </div>

      <div className="mt-2 text-center text-xs text-muted-foreground">
        Ctrl/Cmd + Enter to send
      </div>
    </div>
  );
}
