// src/features/chat/types.ts
export type ChatRole = "system" | "user" | "assistant" | "tool";

export type ChatThread = {
  id: number;
  thread_id: string;
  title: string | null;
  created_by: string;
  metadata_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
};

export type ChatMessage = {
  id: number;
  message_id: string;
  thread_id: string;
  role: ChatRole;
  content: string;
  citations_json: unknown[];
  tool_calls_json: unknown[];
  tool_results_json: unknown[];
  metadata_json: Record<string, unknown>;
  created_at: string;
};

export type ChatThreadDetailResponse = {
  thread: ChatThread;
  messages: ChatMessage[];
};

export type ChatThreadCreate = {
  title?: string | null;
  created_by: string;
  metadata_json?: Record<string, unknown>;
};

export type ChatMessageCreate = {
  content: string;
  use_rag?: boolean;
  max_citations?: number;
  metadata_json?: Record<string, unknown>;
};

export type ChatPostMessageResponse = {
  user_message: ChatMessage;
  assistant_message: ChatMessage;
  proposed_approval_item_id: number | null;
};
