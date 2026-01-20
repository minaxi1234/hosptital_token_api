import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  fetchEmployees,
  fetchDoctors,
  fetchNurses,
  fetchStaff,
  createDoctor,
  createNurse,
  createStaff,
  updateDoctor,
  updateNurse,
  updateStaff,
  deleteDoctor,
  deleteNurse,
  deleteStaff,
} from "../api/admin";

import { createUser } from "../api/adminUsers";

/* ================= UI HELPERS (STYLE ONLY) ================= */
const card = "bg-white rounded-xl border border-slate-200 shadow-sm";
const cardHeader = "border-b border-slate-200 px-6 py-4";
const cardBody = "px-6 py-5 space-y-4";

const input =
  "w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500";

const btnPrimary =
  "bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50";

const btnDark =
  "bg-slate-800 hover:bg-slate-900 text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50";

const btnDanger =
  "bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium";

export default function AdminDashboard() {
  const navigate = useNavigate();

  /* ================= STATE (UNCHANGED) ================= */
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [manageLoading, setManageLoading] = useState(false);

  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const [employees, setEmployees] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [nurses, setNurses] = useState([]);
  const [staffMembers, setStaffMembers] = useState([]);

  const [newEmail, setNewEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [newRoles, setNewRoles] = useState([]);
  const [userSuccess, setUserSuccess] = useState("");

  const [role, setRole] = useState("doctor");
  const [userId, setUserId] = useState("");
  const [specialty, setSpecialty] = useState("");
  const [fee, setFee] = useState("");
  const [department, setDepartment] = useState("");

  const [manageRole, setManageRole] = useState("doctor");
  const [roleList, setRoleList] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState("");
  const [editSpecialty, setEditSpecialty] = useState("");
  const [editFee, setEditFee] = useState("");
  const [editDepartment, setEditDepartment] = useState("");

  /* ================= HELPERS ================= */
  const showSuccess = (msg) => {
    setSuccessMsg(msg);
    setErrorMsg("");
    setTimeout(() => setSuccessMsg(""), 3000);
  };

  const showError = (msg) => {
    setErrorMsg(msg);
    setSuccessMsg("");
    setTimeout(() => setErrorMsg(""), 4000);
  };

  /* ================= LOADERS ================= */
  const loadEmployees = async () => {
    setLoading(true);
    const res = await fetchEmployees();
    setEmployees(res.data);
    setLoading(false);
  };

  const loadRoleLists = async () => {
    const [d, n, s] = await Promise.all([
      fetchDoctors(),
      fetchNurses(),
      fetchStaff(),
    ]);
    setDoctors(d.data);
    setNurses(n.data);
    setStaffMembers(s.data);
  };

  const loadRoleData = async (role) => {
    setManageLoading(true);
    let res;
    if (role === "doctor") res = await fetchDoctors();
    if (role === "nurse") res = await fetchNurses();
    if (role === "staff") res = await fetchStaff();
    setRoleList(res.data);
    setManageLoading(false);
  };

  useEffect(() => {
    loadEmployees();
    loadRoleLists();
  }, []);

  useEffect(() => {
    loadRoleData(manageRole);
    setSelectedEntity("");
    setEditSpecialty("");
    setEditFee("");
    setEditDepartment("");
  }, [manageRole]);

  /* ================= ACTIONS ================= */
  const handleSelectEntity = (id) => {
    const entity = roleList.find((e) => e.id === id);
    setSelectedEntity(id);
    if (!entity) return;

    if (manageRole === "doctor") {
      setEditSpecialty(entity.specialty);
      setEditFee(entity.consultation_fee);
    } else {
      setEditDepartment(entity.department);
    }
  };

  const handleUpdate = async () => {
    try {
      if (manageRole === "doctor") {
        await updateDoctor(selectedEntity, {
          specialty: editSpecialty,
          consultation_fee: Number(editFee),
        });
      }
      if (manageRole === "nurse") {
        await updateNurse(selectedEntity, { department: editDepartment });
      }
      if (manageRole === "staff") {
        await updateStaff(selectedEntity, { department: editDepartment });
      }
      showSuccess("Updated successfully");
      loadRoleData(manageRole);
      loadEmployees();
    } catch {
      showError("Update failed");
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure?")) return;
    try {
      if (manageRole === "doctor") await deleteDoctor(selectedEntity);
      if (manageRole === "nurse") await deleteNurse(selectedEntity);
      if (manageRole === "staff") await deleteStaff(selectedEntity);
      showSuccess("Deleted successfully");
      setSelectedEntity("");
      loadRoleData(manageRole);
      loadEmployees();
    } catch {
      showError("Delete failed");
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await createUser({
        email: newEmail,
        password: newPassword,
        roles: newRoles,
        is_active: true,
      });
      setEmployees((p) => [...p, res.data]);
      setNewEmail("");
      setNewPassword("");
      setNewRoles([]);
      showSuccess("User created successfully");
    } catch {
      showError("User creation failed");
    } finally {
      setSubmitting(false);
    }
  };

  const handleAddEmployee = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      if (role === "doctor") {
        await createDoctor({
          user_id: userId,
          specialty,
          consultation_fee: Number(fee),
        });
      }
      if (role === "nurse") {
        await createNurse({ user_id: userId, department });
      }
      if (role === "staff") {
        await createStaff({ user_id: userId, department });
      }
      showSuccess(`${role} added successfully`);
      setUserId("");
      setSpecialty("");
      setFee("");
      setDepartment("");
      loadEmployees();
      loadRoleLists();
    } catch {
      showError("Add employee failed");
    } finally {
      setSubmitting(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  if (loading) {
    return <p className="text-center mt-20 text-slate-500">Loading...</p>;
  }

  /* ================= UI ================= */
  return (
    <div className="min-h-screen bg-slate-100">
      {/* HEADER */}
      <header className="bg-emerald-700 text-white shadow">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-semibold">Admin Dashboard</h1>
            <p className="text-sm text-emerald-100">
              Hospital staff & token management
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate("/assistant")}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-md text-sm"
            >
              Assistant
            </button>
            <button
              onClick={handleLogout}
              className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-md text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* MESSAGES */}
      <div className="max-w-7xl mx-auto px-6 mt-4 space-y-2">
        {successMsg && (
          <div className="bg-emerald-100 text-emerald-800 border border-emerald-300 rounded px-4 py-2 text-sm">
            {successMsg}
          </div>
        )}
        {errorMsg && (
          <div className="bg-red-100 text-red-800 border border-red-300 rounded px-4 py-2 text-sm">
            {errorMsg}
          </div>
        )}
      </div>

      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT PANEL */}
        <div className="space-y-6">
          {/* CREATE USER */}
          <section className={card}>
            <div className={cardHeader}>
              <h2 className="font-semibold">Create User</h2>
            </div>
            <div className={cardBody}>
              <form onSubmit={handleCreateUser} className="space-y-3">
                <input className={input} placeholder="Email" value={newEmail} onChange={(e) => setNewEmail(e.target.value)} />
                <input className={input} type="password" placeholder="Password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
                <select className={input} value={newRoles[0] || ""} onChange={(e) => setNewRoles([e.target.value])}>
                  <option value="">Select role</option>
                  <option value="admin">Admin</option>
                  <option value="doctor">Doctor</option>
                  <option value="nurse">Nurse</option>
                  <option value="staff">Staff</option>
                </select>
                <button className={`w-full ${btnPrimary}`} disabled={submitting}>
                  Create User
                </button>
              </form>
            </div>
          </section>

          {/* ADD EMPLOYEE */}
          <section className={card}>
            <div className={cardHeader}>
              <h2 className="font-semibold">Add Employee</h2>
            </div>
            <div className={cardBody}>
              <form onSubmit={handleAddEmployee} className="space-y-3">
                <select className={input} value={role} onChange={(e) => setRole(e.target.value)}>
                  <option value="doctor">Doctor</option>
                  <option value="nurse">Nurse</option>
                  <option value="staff">Staff</option>
                </select>

                <select className={input} value={userId} onChange={(e) => setUserId(e.target.value)}>
                  <option value="">Select User</option>
                  {employees.map((e) => (
                    <option key={e.id} value={e.id}>
                      {e.email}
                    </option>
                  ))}
                </select>

                {role === "doctor" && (
                  <>
                    <input className={input} placeholder="Specialty" value={specialty} onChange={(e) => setSpecialty(e.target.value)} />
                    <input className={input} type="number" placeholder="Consultation Fee" value={fee} onChange={(e) => setFee(e.target.value)} />
                  </>
                )}

                {(role === "nurse" || role === "staff") && (
                  <input className={input} placeholder="Department" value={department} onChange={(e) => setDepartment(e.target.value)} />
                )}

                <button className={`w-full ${btnDark}`} disabled={submitting}>
                  Add {role}
                </button>
              </form>
            </div>
          </section>

          {/* MANAGE EMPLOYEE */}
          <section className={card}>
            <div className={cardHeader}>
              <h2 className="font-semibold">Manage Employee</h2>
            </div>
            <div className={cardBody}>
              <select className={input} value={manageRole} onChange={(e) => setManageRole(e.target.value)}>
                <option value="doctor">Doctor</option>
                <option value="nurse">Nurse</option>
                <option value="staff">Staff</option>
              </select>

              <select className={input} value={selectedEntity} onChange={(e) => handleSelectEntity(e.target.value)}>
                <option value="">Select</option>
                {roleList.map((e) => (
                  <option key={e.id} value={e.id}>
                    {e.email}
                  </option>
                ))}
              </select>

              {selectedEntity && manageRole === "doctor" && (
                <>
                  <input className={input} value={editSpecialty} onChange={(e) => setEditSpecialty(e.target.value)} placeholder="Specialty" />
                  <input className={input} type="number" value={editFee} onChange={(e) => setEditFee(e.target.value)} placeholder="Consultation Fee" />
                </>
              )}

              {selectedEntity && manageRole !== "doctor" && (
                <input className={input} value={editDepartment} onChange={(e) => setEditDepartment(e.target.value)} placeholder="Department" />
              )}

              <div className="flex gap-2 pt-2">
                <button onClick={handleUpdate} className={`flex-1 ${btnPrimary}`}>
                  Update
                </button>
                <button onClick={handleDelete} className={`flex-1 ${btnDanger}`}>
                  Delete
                </button>
              </div>
            </div>
          </section>
        </div>

        {/* RIGHT PANEL */}
        <section className="lg:col-span-2 space-y-6">
          {/* STATS */}
          <div className="grid grid-cols-3 gap-4">
            <div className={card}><div className={cardBody}><p className="text-sm text-slate-500">Doctors</p><p className="text-2xl font-semibold">{doctors.length}</p></div></div>
            <div className={card}><div className={cardBody}><p className="text-sm text-slate-500">Nurses</p><p className="text-2xl font-semibold">{nurses.length}</p></div></div>
            <div className={card}><div className={cardBody}><p className="text-sm text-slate-500">Staff</p><p className="text-2xl font-semibold">{staffMembers.length}</p></div></div>
          </div>

          {/* LISTS */}
          <div className={card}>
            <div className={cardHeader}>
              <h2 className="font-semibold">Employees</h2>
            </div>
            <div className="px-6 py-4 space-y-6">
              <div>
                <h3 className="font-medium mb-2">Doctors</h3>
                {doctors.map((d) => (
                  <div key={d.id} className="flex justify-between text-sm border-b py-2">
                    <span>{d.email}</span>
                    <span>{d.specialty} · ₹{d.consultation_fee}</span>
                  </div>
                ))}
              </div>

              <div>
                <h3 className="font-medium mb-2">Nurses</h3>
                {nurses.map((n) => (
                  <div key={n.id} className="flex justify-between text-sm border-b py-2">
                    <span>{n.email}</span>
                    <span>{n.department}</span>
                  </div>
                ))}
              </div>

              <div>
                <h3 className="font-medium mb-2">Staff</h3>
                {staffMembers.map((s) => (
                  <div key={s.id} className="flex justify-between text-sm border-b py-2">
                    <span>{s.email}</span>
                    <span>{s.department}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
