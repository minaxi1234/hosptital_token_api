import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "../auth/Login";
import AdminDashboard from "../pages/AdminDashboard";
import DoctorDashboard from "../pages/DoctorDashboard";
import StaffDashboard from "../pages/StaffDashboard";
import Unauthorized from "../pages/Unauthorized";
import ProtectedRoute from "./ProtectedRoute";
import RoleProtectedRoute from "./RoleProtectedRoute";
import NurseDashboard from "../pages/NurseDashboard";
import TokenDisplay from "../pages/TokenDisplay";
import AssistantPage from "../pages/AssistantPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <RoleProtectedRoute allowedRoles={["admin"]}>
                <AdminDashboard />
              </RoleProtectedRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/doctor"
          element={
            <ProtectedRoute>
              <RoleProtectedRoute allowedRoles={["doctor", "admin"]}>
                <DoctorDashboard />
              </RoleProtectedRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/nurse"
          element={
            <ProtectedRoute>
              <RoleProtectedRoute allowedRoles={["staff", "nurse"]}>
                <NurseDashboard />
              </RoleProtectedRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/staff"
          element={
            <ProtectedRoute>
              <RoleProtectedRoute allowedRoles={["staff", "admin"]}>
                <StaffDashboard />
              </RoleProtectedRoute>
            </ProtectedRoute>
          }
        />
        <Route path="/display" element={<TokenDisplay />} />

    

       <Route path="/assistant" element={<AssistantPage />} />

        <Route path="/unauthorized" element={<Unauthorized />} />
      </Routes>
    </BrowserRouter>
  );
}
