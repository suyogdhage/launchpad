import { useMutation, useQuery } from "@tanstack/react-query";
import api from "../lib/axios";
import type { ChatRequest, ChatResponse } from "../types/api";

export function useChat() {
  return useMutation({
    mutationFn: (data: ChatRequest) =>
      api.post<ChatResponse>("/buddy/chat", data).then((r) => r.data),
  });
}

export function useChatHistory() {
  return useQuery({
    queryKey: ["buddy", "history"],
    queryFn: () =>
      api
        .get<{ role: "user" | "assistant"; content: string }[]>("/buddy/history")
        .then((r) => r.data),
  });
}
