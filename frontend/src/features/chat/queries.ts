// src/features/chat/queries.ts
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type {
  ChatMessageCreate,
  ChatPostMessageResponse,
  ChatThreadCreate,
  ChatThread,
  ChatThreadDetailResponse,
} from "./types";

export function useChatThread(threadId?: string) {
  return useQuery({
    queryKey: ["chat", "thread", threadId],
    enabled: !!threadId,
    queryFn: async () => {
      const res = await api.get<ChatThreadDetailResponse>(`/chat/threads/${threadId}`);
      return res.data;
    },
    staleTime: 5_000,
  });
}

export function useCreateChatThread() {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: async (body: ChatThreadCreate) => {
      const res = await api.post<ChatThread>(`/chat/threads`, body);
      return res.data;
    },
    onSuccess: (thread) => {
      qc.setQueryData(["chat", "thread", thread.thread_id], { thread, messages: [] });
    },
  });
}

export function usePostChatMessage(threadId: string) {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: async (body: ChatMessageCreate) => {
      const res = await api.post<ChatPostMessageResponse>(`/chat/threads/${threadId}/messages`, body);
      return res.data;
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ["chat", "thread", threadId] });
    },
  });
}
