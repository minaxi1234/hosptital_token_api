// api/public.js
import axios from "./axios";

export const fetchPublicTodayTokens = () =>
  axios.get("/patients/tokens/public/today");
