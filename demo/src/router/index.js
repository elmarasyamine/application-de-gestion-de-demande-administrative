import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";

import HomeDemandeur from "../views/HomeDemandeur.vue";
import TableauDeBord from "../views/demandeur/TableauDeBord.vue";
import SoumettreDemande from "../views/demandeur/SoumettreDemande.vue";
import MesDemandes from "../views/demandeur/MesDemandes.vue";
import MessagerieInterne from "../views/demandeur/MessagerieInterne.vue";
import Profil from "../views/demandeur/Profil.vue";
import DetailDemande from "../views/demandeur/DetailDemande.vue";

import AdminLayout from "../views/layouts/AdminLayout.vue";
import TableauDeBordAdmin from "../views/admin/Tableaudebord.vue";
import Demandes from "../views/admin/Demandes.vue";
import ProfilAdmin from "../views/admin/Profil.vue";
import MessagerieAdmin from "../views/admin/Messagerie.vue";
import StatistiquesAdmin from "../views/admin/Statistiques.vue";
import AdminDashboard from "../views/admin/AdminDashboard.vue";
import DetailDemandeAdmin from "../views/admin/DetailDemandeAdmin.vue";


const routes = [
  { path: "/", component: Home },
  { path: "/about", component: About },
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  {
    path: "/admin",
    component: AdminLayout,
    redirect: "/admin/tableau-de-bord",
    children: [
      { path: "tableau-de-bord", component: TableauDeBordAdmin },
      { path: "demandes", component: Demandes },
      { path: "demande/:id", component: DetailDemandeAdmin },
      { path: "profil", component: ProfilAdmin },
      { path: "messagerie", component: MessagerieAdmin },
      { path: "statistiques", component: StatistiquesAdmin }
    ]
  },

  {
    path: "/demandeur",
    component: HomeDemandeur,
    children: [
      { path: "tableau-de-bord", component: TableauDeBord },
      { path: "soumettre-demande", component: SoumettreDemande },
      { path: "mes-demandes", component: MesDemandes },
      { path: "messagerie", component: MessagerieInterne },
      { path: "profil", component: Profil },
      { path: "detail-demande/:id", component: DetailDemande }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
