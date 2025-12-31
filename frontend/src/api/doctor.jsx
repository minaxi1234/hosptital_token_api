import api from "./axios";


// Fetch all tokens for the logged-in doctor
export const fetchDoctorTokens = () => api.get("/patients/tokens");

// Update token status
export const updateTokenStatus = (tokenId, status) =>
  api.patch(`/patients/tokens/${tokenId}`, { status });
