import api from "./axios";

export const createUser = (data) => {
  return api.post("/auth/create", data);
};

export const fetchUsers = () => {
  return api.get("/auth/users");
};
