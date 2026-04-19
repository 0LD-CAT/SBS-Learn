import api from "./axios";

export const registerUser = async (data) => {
    const response = await api.post("/auth/register", {
        username: data.login,
        email: data.email,
        password: data.password,
    });

    return response.data;
};

export const loginUser = async (data) => {
    const response = await api.post("/auth/login", {
        username_or_email: data.login,
        password: data.password,
    });

    return response.data;
};

export const logoutUser = async () => {
  try {
    await api.post("/auth/logout");
  }
  catch (error) {
    console.warn("Ошибка logout:", error);
  }
  localStorage.removeItem("token");
  localStorage.removeItem("user_id");

  window.location.href = "/login";
};
