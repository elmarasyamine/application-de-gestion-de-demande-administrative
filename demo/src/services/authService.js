import api from "./api";

export async function login(email, password) {
  const response = await api.post("/auth/login", {
    email: email,
    password: password
  });

  return response.data;
}

export async function register(utilisateur, type) {
  // Backend expects 'utilisateur' object in body and optional 'type' query param
  const response = await api.post(`/auth/register?type=${type || 'DEMANDEUR'}`, utilisateur);
  return response.data;
}
