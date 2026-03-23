import api from "./axios";

export const getUserProfile = async () => {
  const response = await api.get("/protected/");
  return response.data;
};