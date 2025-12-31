import api from "./axios";

// 1️⃣ Register patient
export const createPatient = (payload) => {
  return api.post("/patients", payload);
};

// 2️⃣ List all patients
export const fetchPatients = () => {
  return api.get("/patients");
};

// 3️⃣ List doctors (staff-safe)
export const fetchDoctors = () => {
  return api.get("/patients/doctors");
};

// 4️⃣ Generate token
export const createToken = (payload) => {
  return api.post("/patients/token", payload);
};

// 5️⃣ Today tokens
export const fetchTodayTokens = () => {
  const token = localStorage.getItem("access_token");
  return api.get("/patients/tokens/today");
};
