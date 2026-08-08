import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../lib/axios";
import type { RequestCreate, RequestResponse } from "../types/api";

export function useCreateRequest() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: RequestCreate) =>
      api.post("/requests/", data).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["requests"] }),
  });
}

export function useGetMyRequests() {
  return useQuery({
    queryKey: ["requests", "my"],
    queryFn: () =>
      api.get<RequestResponse[]>("/requests/my").then((r) => r.data),
  });
}

export function useGetAllRequests() {
  return useQuery({
    queryKey: ["requests", "all"],
    queryFn: () =>
      api.get<RequestResponse[]>("/requests/all").then((r) => r.data),
  });
}

export function useApproveRequest() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request_id: string) =>
      api.patch(`/requests/${request_id}/approve`).then((r) => r.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["requests"] }),
  });
}

export function useRejectRequest() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request_id: string) =>
      api.patch(`/requests/${request_id}/reject`).then((r) => r.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["requests"] }),
  });
}
