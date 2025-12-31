import api from "./axios";

export const fetchMe = () => {
  return  api.get("/auth/me", {
    headers:{
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    },
  });
};