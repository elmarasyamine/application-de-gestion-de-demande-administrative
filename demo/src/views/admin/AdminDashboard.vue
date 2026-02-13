<template>
  <Tableaudebord
    :requests="requests"
    :activities="activities"
    @approve-request="approveRequest"
    @reject-request="rejectRequest"
  />
</template>

<script>
import Tableaudebord from "./Tableaudebord.vue";
import api from "../../services/api";

export default {
  name: "AdminDashboard",
  components: { Tableaudebord },

  data() {
    return {
      requests: [],
      activities: []
    };
  },

  mounted() {
    this.loadDemandes();
  },

  methods: {
    /* ==========================
       CHARGER LES DEMANDES
       ========================== */
    async loadDemandes() {
      try {
        const res = await api.get("/demandes/");
        this.requests = this.mapDemandes(res.data);

        this.activities = [
          {
            icon: "📄",
            text: "Demandes chargées depuis le serveur",
            time: "à l’instant",
            type: "info"
          }
        ];
      } catch (e) {
        console.error("Erreur chargement demandes", e);
      }
    },

    /* ==========================
       VALIDER UNE DEMANDE
       ========================== */
    async approveRequest(req) {
      try {
        await api.put(`/demandes/valider/${req.id}`);
        this.loadDemandes();

        this.activities.unshift({
          icon: "✅",
          text: `Demande ${req.ref} validée`,
          time: "maintenant",
          type: "success"
        });
      } catch (e) {
        console.error("Erreur validation", e);
      }
    },

    /* ==========================
       REJETER UNE DEMANDE
       ========================== */
    async rejectRequest(req) {
      try {
        await api.put(`/demandes/rejeter/${req.id}`);
        this.loadDemandes();

        this.activities.unshift({
          icon: "❌",
          text: `Demande ${req.ref} rejetée`,
          time: "maintenant",
          type: "warning"
        });
      } catch (e) {
        console.error("Erreur rejet", e);
      }
    },

    /* ==========================
       MAPPING BACKEND → FRONT
       ========================== */
    mapDemandes(demandes) {
      return demandes.map(d => ({
        id: d.id,
        ref: "DEM-" + d.id,
        nom: d.demandeur?.nom || "—",
        type: d.typeDemande || "—",
        date: d.dateCreation
          ? d.dateCreation.split("T")[0]
          : "—",
        priority: "medium",
        status: this.mapStatus(d.status)
      }));
    },

    mapStatus(status) {
      switch (status) {
        case "EN_ATTENTE":
          return "pending";
        case "VALIDEE":
          return "approved";
        case "REJETEE":
          return "rejected";
        default:
          return "pending";
      }
    }
  }
  
};
</script>
