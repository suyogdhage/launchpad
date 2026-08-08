import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../lib/axios";
import type { User } from "../types/api";

export function useGetUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: () => api.get<User[]>("/auth/user").then((r) => r.data),
  });
}

export function useAssignManager() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      user_id,
      manager_id,
    }: {
      user_id: string;
      manager_id: string;
    }) =>
      api
        .patch("/auth/assign", null, {
          params: { user_id, manager_id },
        })
        .then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}

export function useMe() {
  return useQuery({
    queryKey: ["me"],
    queryFn: () => api.get("/auth/me").then((r) => r.data),
  });
}
