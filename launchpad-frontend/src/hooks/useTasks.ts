import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../lib/axios";
import type { TaskSchema, TaskResponse } from "../types/api";

export function useGetMyTasks() {
  return useQuery({
    queryKey: ["tasks", "me"],
    queryFn: () =>
      api.get<TaskResponse[]>("/tasks/me").then((r) => r.data),
  });
}

export function useGetAssignedByMe() {
  return useQuery({
    queryKey: ["tasks", "assigned-by-me"],
    queryFn: () => api.get("/tasks/assigned-by-me").then((r) => r.data),
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TaskSchema) =>
      api.post("/tasks/", data).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["tasks"] }),
  });
}

export function useCompleteTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (task_id: string) =>
      api.patch(`/tasks/${task_id}/complete`).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["tasks"] }),
  });
}
