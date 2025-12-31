import { Navigate } from "react-router-dom";
import { normalizeRoles } from "../utils/roles";


export default function RoleProtectedRoute({ children, allowedRoles }) {
  const storedUser = localStorage.getItem("user");

  if (!storedUser) {
    return <Navigate to="/" replace />;
  }

  const user = JSON.parse(storedUser);

  // normalize role names from backend objects
  const userRoles = normalizeRoles(user.roles);

const hasAccess = allowedRoles.some((role) =>
  userRoles.includes(role.toLowerCase())
);

  if (!hasAccess) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}
