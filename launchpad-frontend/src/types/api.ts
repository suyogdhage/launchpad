export interface UserResponse {
  id: string;
  name: string;
  email: string;
}

export interface CreateUser {
  email: string;
  name: string;
  password: string;
  role_name?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
}

export interface JwtPayload {
  id: string;
  role: "superadmin" | "hr" | "manager" | "new_hire";
  exp: number;
  type: string;
}

export interface TaskSchema {
  title: string;
  description?: string;
  assigned_to: string;
  deadline?: string;
}

export interface TaskResponse {
  id: string;
  title: string;
  description: string;
  status: string;
  deadline?: string;
  assigned_to: string;
  assigned_by: string;
  completed_at?: string;
}

export interface DocumentCreate {
  task_id: string;
}

export interface DocUpdate {
  id: string;
  status: "approved" | "rejected";
  reason?: string;
}

export interface RequestCreate {
  description: string;
}

export interface RequestResponse {
  id: string;
  request_by: string;
  description: string;
  status: string;
  created_at: string;
}

export interface DashboardStats {
  total_new_hires: number;
  completed_tasks: number;
  pending_tasks: number;
  pending_document_reviews: number;
  approved_documents: number;
  rejected_documents: number;
}

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  reply: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role_name: string;
  assigned_to?: string;
}
