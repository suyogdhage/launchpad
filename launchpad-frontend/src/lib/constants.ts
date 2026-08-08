export const ROLES = {
  SUPERADMIN: "superadmin",
  HR: "hr",
  MANAGER: "manager",
  NEW_HIRE: "new_hire",
} as const;

export const TASK_STATUS = {
  PENDING: "pending",
  COMPLETED: "completed",
} as const;

export const DOCUMENT_STATUS = {
  PENDING: "pending",
  APPROVED: "approved",
  REJECTED: "rejected",
} as const;

export const REQUEST_STATUS = {
  PENDING: "pending",
  APPROVED: "approved",
  REJECTED: "rejected",
} as const;

export const WS_URL =
  import.meta.env.VITE_WS_URL || "ws://localhost:8000/dashboard/ws";
