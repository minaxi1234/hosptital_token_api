import { useState } from "react";
import api from "../api/axios";
import { fetchMe } from "../api/auth";
import { useNavigate } from "react-router-dom";
import { normalizeRoles } from "../utils/roles";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/auth/login", {
        email: email,
        password: password,
      });

      console.log("LOGIIN SUCCESS:", response.data);

      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);

      const meResponse = await fetchMe();
      const user = meResponse.data;

      localStorage.setItem("user_email", user.email);
      localStorage.setItem("user", JSON.stringify(user));
      console.log("ME RESPONSE:", user);

      const roles = normalizeRoles(user.roles);

      if (roles.includes("admin")) {
        navigate("/admin");
      } else if (roles.includes("doctor")) {
        navigate("/doctor");
      } else if (roles.includes("staff")) {
        navigate("/staff");
      } else {
        navigate("/unauthorized");
      }
    } catch (error) {
      console.error(
        "LOGIN ERROR:",
        error.response?.data || error.message
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-400 to-sky-600 px-4">
      
      {/* Glass Card */}
      <div className="w-full max-w-md rounded-2xl bg-white/10 backdrop-blur-xl shadow-3xl border bg-gradient-to-br from-emerald-900 to-sky-600 px-4 border-white/20">
        
        <div className="p-8">
          {/* Brand */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-white">
              Hospital Token System
            </h1>
            <p className="text-sm text-slate-900 mt-2">
              Internal access for staff & doctors
            </p>
          </div>

          {/* Form */}
          <form className="space-y-5" onSubmit={handleLogin}>
            
            <div>
              <label className="block text-sm  text-slate-900 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="email@example.com"
                className="w-full rounded-lg bg-white/90 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-sm text-slate-900 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className="w-full rounded-lg bg-white/50 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2.5 rounded-lg font-medium transition"
            >
              Sign In
            </button>
          </form>

          {/* Footer */}
          <p className="text-center text-xs text-slate-800 mt-8">
            © {new Date().getFullYear()} Hospital Token Management
          </p>
        </div>
      </div>
    </div>
  );
}
