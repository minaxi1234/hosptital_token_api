import api from "./axios";

export const fetchEmployees = () => {
  return api.get("/admin/employees");
};

export const createDoctor = (data) => {
  return api.post("/admin/doctor", data)
};
// Add Nurse
export const createNurse = async (payload) => {
  return api.post("/admin/nurse", payload);
};

// Add Staff
export const createStaff = async (payload) => {
  return api.post("/admin/staff", payload);
};

// Fetch role-specific lists
export const fetchDoctors = () => api.get("/admin/doctors");
export const fetchNurses = () => api.get("/admin/nurses");
export const fetchStaff = () => api.get("/admin/staff");

// Update
export const updateDoctor = (id, payload) =>
  api.put(`/admin/doctor/${id}`, payload);

export const updateNurse = (id, payload) =>
  api.put(`/admin/nurse/${id}`, payload);

export const updateStaff = (id, payload) =>
  api.put(`/admin/staff/${id}`, payload);

// Delete
export const deleteDoctor = (id) =>
  api.delete(`/admin/doctor/${id}`);

export const deleteNurse = (id) =>
  api.delete(`/admin/nurse/${id}`);

export const deleteStaff = (id) =>
  api.delete(`/admin/staff/${id}`);
