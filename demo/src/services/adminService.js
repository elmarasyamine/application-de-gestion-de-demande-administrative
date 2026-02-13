import api from "./api";

export function getAllAdministrateurs() {
    return api.get("/admin/administrateurs/");
}

export function getAdministrateurById(id) {
    return api.get(`/admin/administrateurs/${id}`);
}

export function createAdministrateur(admin) {
    return api.post("/admin/administrateurs", admin);
}

export function deleteAdministrateur(id) {
    return api.delete(`/admin/administrateurs/${id}`);
}

export function updatePassword(id, newPassword) {
    // Pass as QueryParam as per backend @RequestParam
    return api.put(`/admin/administrateurs/${id}/password?newPassword=${newPassword}`);
}

export function updateAdministrateur(id, admin) {
    return api.put(`/admin/administrateurs/${id}`, admin);
}
