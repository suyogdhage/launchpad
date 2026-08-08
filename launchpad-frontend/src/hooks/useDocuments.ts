import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "../lib/axios";
import type { DocUpdate } from "../types/api";

export function useGetMyDocuments() {
  return useQuery({
    queryKey: ["documents"],
    queryFn: () => api.get("/document/my").then((r) => r.data),
  });
}

export function useGetPendingDocuments() {
  return useQuery({
    queryKey: ["documents", "pending"],
    queryFn: () => api.get("/document/pending").then((r) => r.data),
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      task_id,
      file,
    }: {
      task_id: string;
      file: File;
    }) => {
      const formData = new FormData();
      formData.append("task_id", task_id);
      formData.append("file", file);
      return api.post("/document/create", formData).then((r) => r.data);
    },
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["documents"] }),
  });
}

export function useApproveDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (document_id: string) =>
      api
        .patch("/document/approve", null, {
          params: { document_id },
        })
        .then((r) => r.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["documents"] }),
  });
}

export function useRejectDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      document_id,
      reason,
    }: {
      document_id: string;
      reason: string;
    }) =>
      api
        .patch("/document/reject", null, {
          params: { document_id, reason },
        })
        .then((r) => r.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["documents"] }),
  });
}

export function useUpdateDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: DocUpdate) =>
      api.patch("/document/update", data).then((r) => r.data),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["documents"] }),
  });
}

export async function downloadDocument(documentId: string, filename?: string) {
  const res = await api.get(`/document/download/${documentId}`, {
    responseType: "blob",
  });
  const blob = res.data as Blob;
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename || "document";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}
