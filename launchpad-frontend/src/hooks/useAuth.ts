import { useMutation } from "@tanstack/react-query";
import api from "../lib/axios";
import type { UserLogin, LoginResponse, CreateUser } from "../types/api";

export function useLogin() {
  return useMutation({
    mutationFn: (data: UserLogin) =>
      api.post<LoginResponse>("/auth/login", data).then((r) => r.data),
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (data: CreateUser) =>
      api.post("/auth/register", data).then((r) => r.data),
  });
}
