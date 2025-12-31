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

export default function AdminDashboard() {
  // --------------------
  // NAVIGATION
  // --------------------
  const navigate = useNavigate();

  // --------------------
  // GLOBAL STATE
  // --------------------
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [manageLoading, setManageLoading] = useState(false);

    // --------------------
    // GLOBAL UI MESSAGES
    // --------------------
    const [successMsg, setSuccessMsg] = useState("");
    const [errorMsg, setErrorMsg] = useState("");

  // --------------------
  // USERS (for dropdown)
  // --------------------
  const [employees, setEmployees] = useState([]);

  // --------------------
  // ROLE LISTS (right panel)
  // --------------------
  const [doctors, setDoctors] = useState([]);
  const [nurses, setNurses] = useState([]);
  const [staffMembers, setStaffMembers] = useState([]);

  // --------------------
  // CREATE USER
  // --------------------
  const [newEmail, setNewEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [newRoles, setNewRoles] = useState([]);
  const [userSuccess, setUserSuccess] = useState("");

  // --------------------
  // ADD EMPLOYEE
  // --------------------
  const [role, setRole] = useState("doctor");
  const [userId, setUserId] = useState("");
  const [specialty, setSpecialty] = useState("");
  const [fee, setFee] = useState("");
  const [department, setDepartment] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  // --------------------
  // MANAGE EMPLOYEE
  // --------------------
  const [manageRole, setManageRole] = useState("doctor");
  const [roleList, setRoleList] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState("");

  const [editSpecialty, setEditSpecialty] = useState("");
  const [editFee, setEditFee] = useState("");
  const [editDepartment, setEditDepartment] = useState("");


  
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

  // --------------------
  // LOAD USERS
  // --------------------
  const loadEmployees = async () => {
    setLoading(true);
    try {
      const res = await fetchEmployees();
      setEmployees(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // --------------------
  // LOAD ROLE LISTS (RIGHT PANEL)
  // --------------------
  const loadRoleLists = async () => {
    try {
      const [d, n, s] = await Promise.all([
        fetchDoctors(),
        fetchNurses(),
        fetchStaff(),
      ]);

      setDoctors(d.data);
      setNurses(n.data);
      setStaffMembers(s.data);
    } catch (err) {
      console.error(err);
    }
  };

  // --------------------
  // LOAD MANAGE LIST
  // --------------------
  const loadRoleData = async (role) => {
    setManageLoading(true);
    try {
      let res;
      if (role === "doctor") res = await fetchDoctors();
      if (role === "nurse") res = await fetchNurses();
      if (role === "staff") res = await fetchStaff();

      setRoleList(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setManageLoading(false);
    }
  };

  // --------------------
  // INITIAL LOAD
  // --------------------
  useEffect(() => {
    loadEmployees();
    loadRoleLists();
  }, []);

  // --------------------
  // MANAGE ROLE CHANGE
  // --------------------
  useEffect(() => {
    loadRoleData(manageRole);
    setSelectedEntity("");
    setEditSpecialty("");
    setEditFee("");
    setEditDepartment("");
  }, [manageRole]);

  // --------------------
  // SELECT ENTITY
  // --------------------
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

  // --------------------
  // UPDATE
  // --------------------
  const handleUpdate = async () => {
    try {
      if (manageRole === "doctor") {
        await updateDoctor(selectedEntity, {
          specialty: editSpecialty,
          consultation_fee: Number(editFee),
        });
      }

      if (manageRole === "nurse") {
        await updateNurse(selectedEntity, {
          department: editDepartment,
        });
      }

      if (manageRole === "staff") {
        await updateStaff(selectedEntity, {
          department: editDepartment,
        });
      }

      showSuccess("Updated successfully");
      loadRoleData(manageRole);
      loadEmployees();
    } catch (err) {
      console.error(err);
      showError("Update failed");
    }
  };

  // --------------------
  // DELETE
  // --------------------
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
    } catch (err) {
  console.error(err);

  const message =
    err.response?.data?.detail ||
    "Delete failed";

  showError(message);
}

  };

  // --------------------
  // CREATE USER
  // --------------------
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

      setEmployees((prev) => [...prev, res.data]);
      setNewEmail("");
      setNewPassword("");
      setNewRoles([]);

      setUserSuccess("User created successfully!");
      setTimeout(() => setUserSuccess(""), 3000);
    } catch (err) {
      console.error(err.response?.data || err.message);
      showError("Failed to create user");
    } finally {
      setSubmitting(false);
    }
  };

  // --------------------
  // ADD EMPLOYEE
  // --------------------
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

      setSuccessMessage(`${role} added successfully!`);
      setTimeout(() => setSuccessMessage(""), 3000);

      setUserId("");
      setSpecialty("");
      setFee("");
      setDepartment("");

      loadEmployees();
      loadRoleLists();
    } catch (err) {
      console.error(err.response?.data || err.message);
      showError("Failed to add employee");
    } finally {
      setSubmitting(false);
    }
  };

  // --------------------
  // LOGOUT
  // --------------------
  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  if (loading) {
    return <p className="text-center mt-20 text-slate-500">Loading employees...</p>;
  }



  return (
  <div className="min-h-screen bg-slate-100">
    {/* Header */}
    <header className="bg-emerald-700 text-white px-6 py-4 flex justify-between items-center shadow">
      <div>
        <h1 className="text-xl font-semibold">Admin Dashboard</h1>
        <p className="text-sm text-emerald-100">
          Hospital staff & token management
        </p>
      </div>
      <button
        onClick={handleLogout}
        className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-md text-sm"
      >
        Logout
      </button>
    </header>

    {/* Main Content */}
    <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      {successMsg && (
      <div className="mb-4 rounded-md bg-emerald-100 border border-emerald-300 px-4 py-2 text-emerald-800 text-sm">
        {successMsg}
      </div>
    )}

    {errorMsg && (
      <div className="mb-4 rounded-md bg-red-100 border border-red-300 px-4 py-2 text-red-800 text-sm">
        {errorMsg}
      </div>
    )}


      {/* LEFT PANEL */}
      <div className="space-y-6">
        
        {/* Create User */}
        <section className="bg-white rounded-lg shadow p-5">
          <h2 className="text-lg font-semibold mb-4">Create User</h2>

          {userSuccess && (
            <div className="mb-3 text-sm text-emerald-700 bg-emerald-50 border border-emerald-200 rounded p-2">
              {userSuccess}
            </div>
          )}

          <form onSubmit={handleCreateUser} className="space-y-3">
            <input
              placeholder="Email"
              value={newEmail}
              onChange={(e) => setNewEmail(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm"
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm"
              required
            />

            <select
            value={newRoles[0] || ""}
            onChange={(e) => setNewRoles([e.target.value])}
            required
            className="w-full border rounded px-3 py-2 text-sm"
          >
            <option value="" disabled>
              Select role
            </option>
            <option value="admin">Admin</option>
            <option value="doctor">Doctor</option>
            <option value="nurse">Nurse</option>
            <option value="staff">Staff</option>
          </select>


            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded text-sm"
            >
              {submitting ? "Creating..." : "Create User"}
            </button>
          </form>
        </section>

        {/* Add Employee */}
        <section className="bg-white rounded-lg shadow p-5">
          <h2 className="text-lg font-semibold mb-4">Add Employee</h2>

          {successMessage && (
            <div className="mb-3 text-sm text-emerald-700 bg-emerald-50 border border-emerald-200 rounded p-2">
              {successMessage}
            </div>
          )}

          <form onSubmit={handleAddEmployee} className="space-y-3">
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm"
            >
              <option value="doctor">Doctor</option>
              <option value="nurse">Nurse</option>
              <option value="staff">Staff</option>
            </select>

            <select
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm"
              required
            >
              <option value="">Select User</option>
              {employees.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.email}
                </option>
              ))}
            </select>

            {role === "doctor" && (
              <>
                <input
                  placeholder="Specialty"
                  value={specialty}
                  onChange={(e) => setSpecialty(e.target.value)}
                  className="w-full border rounded px-3 py-2 text-sm"
                  required
                />
                <input
                  type="number"
                  placeholder="Consultation Fee"
                  value={fee}
                  onChange={(e) => setFee(e.target.value)}
                  className="w-full border rounded px-3 py-2 text-sm"
                  required
                />
              </>
            )}

            {(role === "nurse" || role === "staff") && (
              <input
                placeholder="Department"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="w-full border rounded px-3 py-2 text-sm"
                required
              />
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-slate-800 hover:bg-slate-900 text-white py-2 rounded text-sm"
            >
              Add {role}
            </button>
          </form>
        </section>

        <section className="bg-white rounded-lg shadow p-5">
  <h2 className="text-lg font-semibold mb-4">Manage Employee</h2>

  <select
    value={manageRole}
    onChange={(e) => setManageRole(e.target.value)}
    className="w-full border rounded px-3 py-2 text-sm mb-3"
  >
    <option value="doctor">Doctor</option>
    <option value="nurse">Nurse</option>
    <option value="staff">Staff</option>
  </select>

  <select
    value={selectedEntity}
    onChange={(e) => handleSelectEntity(e.target.value)}
    className="w-full border rounded px-3 py-2 text-sm mb-3"
  >
    <option value="">Select</option>
    {roleList.map((e) => (
      <option key={e.id} value={e.id}>
        {e.email || "Employee"}
      </option>
    ))}
  </select>

  {selectedEntity && manageRole === "doctor" && (
    <>
      <input
        className="w-full border rounded px-3 py-2 text-sm mb-2"
        value={editSpecialty}
        onChange={(e) => setEditSpecialty(e.target.value)}
        placeholder="Specialty"
      />
      <input
        type="number"
        className="w-full border rounded px-3 py-2 text-sm mb-2"
        value={editFee}
        onChange={(e) => setEditFee(e.target.value)}
        placeholder="Consultation Fee"
      />
    </>
  )}

  {selectedEntity && manageRole !== "doctor" && (
    <input
      className="w-full border rounded px-3 py-2 text-sm mb-2"
      value={editDepartment}
      onChange={(e) => setEditDepartment(e.target.value)}
      placeholder="Department"
    />
  )}

  <div className="flex gap-2 mt-3">
    <button
      onClick={handleUpdate}
      className="flex-1 bg-emerald-600 text-white py-2 rounded text-sm"
    >
      Update
    </button>
    <button
      onClick={handleDelete}
      className="flex-1 bg-red-600 text-white py-2 rounded text-sm"
    >
      Delete
    </button>
  </div>
</section>

      </div>

      {/* RIGHT PANEL */}
      <section className="lg:col-span-2 bg-white rounded-lg shadow p-6 space-y-8">
        <h2 className="text-lg font-semibold">Employees</h2>

        {/* Doctors */}
        <div>
          <h3 className="font-medium text-slate-700 mb-3">Doctors</h3>
          <div className="space-y-2">
          {doctors.map((d) => (
          <div key={d.id} className="flex justify-between border p-2">
            <span>{d.email}</span>
            <span>{d.specialty} · ₹{d.consultation_fee}</span>
          </div>
        ))}

          </div>
        </div>

        {/* Nurses */}
        <div>
          <h3 className="font-medium text-slate-700 mb-3">Nurses</h3>
          <div className="space-y-2">
            {nurses.map((n) => (
            <div key={n.id} className="flex justify-between border p-2">
              <span>{n.email}</span>
              <span>{n.department}</span>
            </div>
          ))}

          </div>
        </div>

        {/* Staff */}
        <div>
          <h3 className="font-medium text-slate-700 mb-3">Staff</h3>
          <div className="space-y-2">
           {staffMembers.map((s) => (
          <div key={s.id} className="flex justify-between border p-2">
            <span>{s.email}</span>
            <span>{s.department}</span>
          </div>
        ))}

          </div>
        </div>
      </section>
    </main>
  </div>
);

}
