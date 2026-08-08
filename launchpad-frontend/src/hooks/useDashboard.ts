import { useQuery } from "@tanstack/react-query";
import api from "../lib/axios";
import type { DashboardStats } from "../types/api";

export function useGetStats() {
  return useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: () =>
      api.get<DashboardStats>("/dashboard/stats").then((r) => r.data),
  });
}
