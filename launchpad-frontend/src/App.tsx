import { Routes, Route, Navigate } from "react-router-dom";
import { AppLayout } from "./components/shared/AppLayout";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { RoleGuard } from "./components/auth/RoleGuard";
import { ROLES } from "./lib/constants";
import { useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import UserManagementPage from "./pages/UserManagementPage";
import RegisterPage from "./pages/RegisterPage";
import TaskListPage from "./pages/TaskListPage";
import CreateTaskPage from "./pages/CreateTaskPage";
import AssignedTasksPage from "./pages/AssignedTasksPage";
import DocumentListPage from "./pages/DocumentListPage";
import PendingReviewsPage from "./pages/PendingReviewsPage";
import RequestListPage from "./pages/RequestListPage";
import AllRequestsPage from "./pages/AllRequestsPage";
import BuddyChatPage from "./pages/BuddyChatPage";
import ProfilePage from "./pages/ProfilePage";

function DefaultHome() {
  const { user } = useAuth();
  const role = user?.role || "new_hire";
  return (
    <Navigate
      to={role === "hr" || role === "superadmin" ? "/dashboard" : "/tasks"}
      replace
    />
  );
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={
          <RoleGuard roles={[ROLES.HR, ROLES.SUPERADMIN]}>
            <DashboardPage />
          </RoleGuard>
        } />
        <Route path="/users" element={
          <RoleGuard roles={[ROLES.HR, ROLES.SUPERADMIN]}>
            <UserManagementPage />
          </RoleGuard>
        } />
        <Route path="/register" element={
          <RoleGuard roles={[ROLES.HR]}>
            <RegisterPage />
          </RoleGuard>
        } />
        <Route path="/tasks" element={<TaskListPage />} />
        <Route path="/tasks/assigned-by-me" element={
          <RoleGuard roles={[ROLES.HR, ROLES.MANAGER, ROLES.SUPERADMIN]}>
            <AssignedTasksPage />
          </RoleGuard>
        } />
        <Route path="/tasks/create" element={
          <RoleGuard roles={[ROLES.HR, ROLES.MANAGER, ROLES.SUPERADMIN]}>
            <CreateTaskPage />
          </RoleGuard>
        } />
        <Route path="/documents" element={<DocumentListPage />} />
        <Route path="/documents/pending" element={
          <RoleGuard roles={[ROLES.HR, ROLES.SUPERADMIN]}>
            <PendingReviewsPage />
          </RoleGuard>
        } />
        <Route path="/requests" element={<RequestListPage />} />
        <Route path="/requests/all" element={
          <RoleGuard roles={[ROLES.MANAGER, ROLES.HR, ROLES.SUPERADMIN]}>
            <AllRequestsPage />
          </RoleGuard>
        } />
        <Route path="/buddy" element={<BuddyChatPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/" element={<DefaultHome />} />
      </Route>
    </Routes>
  );
}

export default App;
