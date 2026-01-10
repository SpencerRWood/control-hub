// src/features/chat/ChatPage.tsx
import * as React from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { useChatThread, useCreateChatThread, usePostChatMessage } from "./queries";
import type { ChatMessage } from "./types";

const STORAGE_KEY = "controlhub.chat.thread_id";

function roleLabel(role: ChatMessage["role"]) {
  if (role === "user") return "You";
  if (role === "assistant") return "Assistant";
  return role;
}

function roleVariant(role: ChatMessage["role"]): "default" | "secondary" | "outline" {
  if (role === "user") return "default";
  if (role === "assistant") return "secondary";
  return "outline";
}

export function ChatPage() {
  const [threadId, setThreadId] = React.useState<string | null>(() => localStorage.getItem(STORAGE_KEY));
  const [input, setInput] = React.useState("");

  const createThread = useCreateChatThread();
  const threadQ = useChatThread(threadId ?? undefined);
  const postMsg = usePostChatMessage(threadId ?? "__unset__");

  const messages = threadQ.data?.messages ?? [];
  const isReady = !!threadId && !createThread.isPending;

  React.useEffect(() => {
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
  }, [threadId, createThread]);

  async function onSend() {
    if (!threadId) return;
    const content = input.trim();
    if (!content || postMsg.isPending) return;

    setInput("");
    postMsg.mutate({
      content,
      use_rag: false,
      max_citations: 0,
      metadata_json: { client: "frontend" },
    });
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col gap-4">
      <Card className="px-4 py-3">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="text-lg font-semibold leading-none">Chat</div>
            <div className="mt-1 text-xs text-muted-foreground truncate">
              Thread: {threadId ?? "creating…"}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              onClick={() => {
                localStorage.removeItem(STORAGE_KEY);
                setThreadId(null);
              }}
            >
              New thread
            </Button>
          </div>
        </div>
      </Card>

      <Card className="flex-1 overflow-hidden">
        <div className="flex h-full flex-col">
          <div className="flex items-center justify-between px-4 py-3">
            <div className="text-sm font-medium">Messages</div>
            <div className="text-xs text-muted-foreground">
              {threadQ.isLoading ? "Loading…" : `${messages.length} message(s)`}
            </div>
          </div>
          <Separator />

          <ScrollArea className="flex-1">
            <div className="space-y-4 p-4">
              {threadQ.isLoading && (
                <div className="text-sm text-muted-foreground">Loading…</div>
              )}

              {!threadQ.isLoading && messages.length === 0 && (
                <div className="rounded-lg border bg-muted/30 p-4 text-sm text-muted-foreground">
                  Start the conversation by sending a message below.
                </div>
              )}

              {messages.map((m) => {
                const isUser = m.role === "user";
                return (
                  <div
                    key={m.message_id}
                    className={["flex", isUser ? "justify-end" : "justify-start"].join(" ")}
                  >
                    <div className={["max-w-[78%]", isUser ? "items-end" : "items-start"].join(" ")}>
                      <div className={["mb-1 flex items-center gap-2", isUser ? "justify-end" : ""].join(" ")}>
                        <Badge variant={roleVariant(m.role)}>{roleLabel(m.role)}</Badge>
                        <span className="text-[11px] text-muted-foreground">
                          {new Date(m.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                        </span>
                      </div>

                      <div
                        className={[
                          "rounded-2xl border px-3 py-2 text-sm leading-relaxed whitespace-pre-wrap shadow-sm",
                          isUser ? "bg-primary text-primary-foreground border-primary/20" : "bg-background",
                        ].join(" ")}
                      >
                        {m.content}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </ScrollArea>

          <Separator />

          <div className="p-4">
            <div className="flex gap-2">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Write a message…"
                className="min-h-[56px] resize-none"
                disabled={!isReady || postMsg.isPending}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                    e.preventDefault();
                    onSend();
                  }
                }}
              />
              <Button onClick={onSend} disabled={!isReady || postMsg.isPending || !input.trim()}>
                Send
              </Button>
            </div>

            <div className="mt-2 text-xs text-muted-foreground">
              Ctrl/Cmd + Enter to send.
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
