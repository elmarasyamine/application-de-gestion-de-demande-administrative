import api from "./api";

export function getAllDemandes() {
  return api.get(`/demandes/?_t=${new Date().getTime()}`);
}

export function getDemandeById(id) {
  return api.get(`/demandes/${id}`);
}

export function soumettreDemande(data) {
  const formData = new FormData();
  formData.append("titreDemande", data.titreDemande);
  formData.append("typeDemande", data.typeDemande);
  formData.append("idDemandeur", data.idDemandeur);
  formData.append("description", data.description);
  if (data.fichier) {
    formData.append("fichier", data.fichier);
  }

  return api.post("/demandes/soumettre", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}

export function assignerDemande(idDemande, idAdmin) {
  return api.put(`/demandes/assign/${idDemande}/${idAdmin}`);
}

export function validerDemande(id) {
  return api.put(`/demandes/valider/${id}`);
}

export function rejeterDemande(id) {
  return api.put(`/demandes/rejeter/${id}`);
}

export function traiterDemande(id) {
  return api.put(`/demandes/traiter/${id}`);
}

export function filtrerDemandes(status) {
  return api.get(`/demandes/filtrer?status=${status}`);
}

export function getMesDemandes(idDemandeur) {
  return api.get(`/demandes/mes-demandes/${idDemandeur}`);
}
