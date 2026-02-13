<template>
  <div class="flex h-screen bg-gray-100 overflow-hidden">
    
    <!-- SIDEBAR -->
    <aside 
      :class="[
        'bg-gradient-to-b from-indigo-600 via-purple-600 to-indigo-800 text-white transition-all duration-300 flex flex-col',
        sidebarCollapsed ? 'w-20' : 'w-64'
      ]"
    >
      <!-- Sidebar Header -->
      <div class="p-6 border-b border-white/20">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center text-2xl backdrop-blur-sm">
            <BarChart3 class="w-6 h-6" />
          </div>
          <transition name="fade">
            <div v-if="!sidebarCollapsed" class="flex-1">
              <h2 class="text-xl font-bold">AdminPanel</h2>
              <p class="text-xs text-white/70">Plateforme de gestion</p>
            </div>
          </transition>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-6 space-y-2 overflow-y-auto">
        <router-link 
          to="/admin/tableau-de-bord" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <BarChart3 class="w-6 h-6" />
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Tableau de bord
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/admin/demandes" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <FileText class="w-6 h-6" />
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Demandes
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/admin/messagerie" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <MessageCircle class="w-6 h-6" />
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Messagerie
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/admin/statistiques" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <TrendingUp class="w-6 h-6" />
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Statistiques
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/admin/profil" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <User class="w-6 h-6" />
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Mon Profil
            </span>
          </transition>
        </router-link>
      </nav>
    </aside>

    <!-- MAIN CONTENT -->
    <div class="flex-1 flex flex-col overflow-hidden">
      
      <!-- HEADER -->
      <header class="bg-white border-b border-gray-200 shadow-sm">
        <div class="flex items-center justify-between px-6 py-4">
          
          <!-- Header Left -->
          <div class="flex items-center gap-4 flex-1">
            <button 
              @click="toggleSidebar"
              class="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-gray-100 transition-colors"
            >
              <Menu class="w-6 h-6" />
            </button>
            
            <div class="relative max-w-md w-full">
              <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                type="text" 
                placeholder="Rechercher..."
                v-model="globalSearch"
                @input="handleGlobalSearch"
                class="w-full pl-12 pr-4 py-2.5 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
              />
            </div>
          </div>

          <!-- Header Right -->
          <div class="flex items-center gap-4">
            <!-- Notifications -->
            <div class="relative">
              <button 
                @click="toggleNotifications"
                class="relative w-10 h-10 flex items-center justify-center rounded-xl hover:bg-gray-100 transition-colors"
              >
                <span class="text-2xl">🔔</span>
                <span 
                  v-if="unreadMessages > 0" 
                  class="absolute top-1 right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center"
                >
                  {{ unreadMessages }}
                </span>
              </button>

              <!-- Notification Dropdown -->
              <transition name="dropdown">
                <div 
                  v-if="showNotifications" 
                  class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden z-50"
                >
                  <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-gray-50">
                    <h3 class="font-semibold text-gray-800">Notifications</h3>
                    <button 
                      @click="markAllAsRead"
                      class="text-xs text-indigo-600 hover:text-indigo-700 font-medium"
                    >
                      Tout marquer comme lu
                    </button>
                  </div>
                  <div class="max-h-96 overflow-y-auto">
                    <div 
                      v-for="notif in notifications" 
                      :key="notif.id"
                      @click="markAsRead(notif.id)"
                      :class="[
                        'px-4 py-3 border-b border-gray-100 cursor-pointer transition-colors hover:bg-gray-50',
                        notif.unread ? 'bg-indigo-50' : ''
                      ]"
                    >
                      <div class="font-medium text-gray-800 mb-1">{{ notif.text }}</div>
                      <div class="text-sm text-gray-500">{{ notif.time }}</div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>

            <!-- User Profile -->
            <div class="flex items-center gap-3 pl-4 border-l border-gray-300">
              <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-md">
                {{ adminName.charAt(0) }}
              </div>
              <div class="hidden lg:block">
                <div class="font-semibold text-gray-800">{{ adminName }}</div>
                <div class="text-xs text-gray-500">Administrateur</div>
              </div>
            </div>

            <!-- Logout Button -->
            <button 
              @click="handleLogout"
              class="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition-colors font-medium"
            >
              <span class="text-lg">🚪</span>
              <span class="hidden md:inline">Déconnexion</span>
            </button>
          </div>
        </div>
      </header>

      <!-- ROUTER VIEW -->
      <main class="flex-1 overflow-y-auto p-6 bg-gray-50">
        <router-view 
          :requests="requests"
          :activities="activities"
          @approve-request="approveRequest"
          @reject-request="rejectRequest"
          @update-request="updateRequest"
        />
      </main>

    </div>

    <!-- Toast Notification -->
    <transition name="toast">
      <div 
        v-if="toast.show"
        :class="[
          'fixed bottom-6 right-6 px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 z-50 min-w-[300px]',
          toast.type === 'success' ? 'bg-green-500 text-white' : '',
          toast.type === 'error' ? 'bg-red-500 text-white' : '',
          toast.type === 'info' ? 'bg-blue-500 text-white' : ''
        ]"
      >
        <span class="text-2xl">{{ toast.icon }}</span>
        <span class="font-medium">{{ toast.message }}</span>
      </div>
    </transition>

    <!-- Confirmation Modal -->
    <transition name="modal">
      <div 
        v-if="modal.show" 
        class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 px-4"
        @click.self="modal.show = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <h3 class="text-xl font-bold text-gray-800">{{ modal.title }}</h3>
            <button 
              @click="modal.show = false"
              class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors text-2xl leading-none"
            >
              ×
            </button>
          </div>
          <div class="px-6 py-6">
            <p class="text-gray-600">{{ modal.message }}</p>
          </div>
          <div class="flex items-center justify-end gap-3 px-6 py-4 bg-gray-50 border-t border-gray-200">
            <button 
              @click="modal.show = false"
              class="px-5 py-2.5 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-100 transition-colors"
            >
              Annuler
            </button>
            <button 
              @click="modal.onConfirm"
              class="px-5 py-2.5 rounded-xl bg-red-600 text-white font-medium hover:bg-red-700 transition-colors"
            >
              Confirmer
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>
import { BarChart3, FileText, MessageCircle, TrendingUp, User, Menu, Search, Bell, MoreVertical, LogOut, Mail } from 'lucide-vue-next';
import { getAllDemandes, validerDemande, rejeterDemande } from '../../services/demandeService';
import { getAdministrateurById } from '../../services/adminService';

export default {
  name: 'AdminLayout',
  components: { BarChart3, FileText, MessageCircle, TrendingUp, User, Menu, Search, Bell, MoreVertical, LogOut, Mail },
  data() {
    return {
      sidebarCollapsed: false,
      globalSearch: '',
      adminName: 'Admin Principal',
      showNotifications: false,
      unreadMessages: 0,
      loading: false,
      notifications: [],
      requests: [],
      activities: [],
      toast: {
        show: false,
        type: '',
        icon: '',
        message: ''
      },
      modal: {
        show: false,
        title: '',
        message: '',
        onConfirm: null
      }
    };
  },
  watch: {
    '$route'() {
      // Recharger les données à chaque changement de page pour garantir la fraîcheur (ex: retour de détail vers liste)
      this.fetchDemandes();
    }
  },
  async created() {
    await this.loadAdminInfo();
    await this.fetchDemandes();
    // Refresh périodique toutes les 30s
    this.polling = setInterval(this.fetchDemandes, 30000);
  },
  methods: {
    async loadAdminInfo() {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      
      // 1. Affichage immédiat (cache)
      if (user && user.nom) {
        this.adminName = `${user.prenom || ''} ${user.nom}`.trim() || 'Administrateur';
      }

      // 2. Synchronisation avec la base de données (réel)
      if (user && user.id) {
        try {
          const response = await getAdministrateurById(user.id);
          const admin = response.data;
          if (admin) {
            this.adminName = `${admin.prenom || ''} ${admin.nom}`.trim();
          }
        } catch (error) {
          console.error('Erreur chargement profil admin:', error);
        }
      }
    },
    async fetchDemandes() {
      this.loading = true;
      try {
        const response = await getAllDemandes();
        // Utiliser les données brutes du backend pour garantir la cohérence
        this.requests = response.data || [];
        
        // Générer les activités basées sur les demandes récentes (avec champs backend)
        this.activities = this.requests.slice(0, 5).map(req => ({
          icon: req.status === 'VALIDEE' ? 'Check' : req.status === 'REJETEE' ? 'X' : 'FileText',
          text: `Demande ${req.reference} - ${req.demandeur?.nom || 'Inconnu'}`,
          time: this.formatDate(req.dateDepot),
          type: req.status === 'VALIDEE' ? 'success' : req.status === 'REJETEE' ? 'warning' : 'info'
        }));

        // Compter les demandes en attente comme notifications
        this.unreadMessages = this.requests.filter(r => r.status === 'SOUMISE').length;
        this.notifications = this.requests
          .filter(r => r.status === 'SOUMISE')
          .slice(0, 5)
          .map((req, index) => ({
            id: index + 1,
            text: `Demande ${req.reference} en attente de ${req.demandeur?.nom || 'Inconnu'}`,
            unread: true,
            time: this.formatDate(req.dateDepot)
          }));

      } catch (error) {
        console.error('Erreur lors du chargement des demandes:', error);
        this.showToast('error', '❌', 'Erreur lors du chargement des demandes');
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        });
      } catch {
        return dateString;
      }
    },
    assignPriority(demande) {
      // Assigner une priorité basée sur l'ancienneté de la demande
      if (!demande.dateDepot) return 'medium';
      const daysDiff = Math.floor((new Date() - new Date(demande.dateDepot)) / (1000 * 60 * 60 * 24));
      if (daysDiff > 7) return 'high';
      if (daysDiff > 3) return 'medium';
      return 'low';
    },
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
    },
    markAsRead(id) {
      const notif = this.notifications.find(n => n.id === id);
      if (notif) notif.unread = false;
    },
    markAllAsRead() {
      this.notifications.forEach(n => n.unread = false);
    },
    handleGlobalSearch() {
      console.log('Recherche globale:', this.globalSearch);
    },
    handleLogout() {
      this.showModal(
        'Déconnexion',
        'Êtes-vous sûr de vouloir vous déconnecter ?',
        () => {
          this.showToast('info', 'Info', 'Déconnexion en cours...');
          setTimeout(() => {
            localStorage.removeItem('authToken');
            this.$router.push('/login');
          }, 1000);
        }
      );
    },
    async approveRequest(req) {
      try {
        await validerDemande(req.id);
        const index = this.requests.findIndex(r => r.id === req.id);
        if (index !== -1) {
          this.requests[index].status = 'VALIDEE';
        }
        this.activities.unshift({
          icon: 'Check',
          text: `Demande ${req.reference} validée`,
          time: 'À l\'instant',
          type: 'success'
        });
        this.showToast('success', '✅', `Demande ${req.reference} validée avec succès`);
        // Rafraîchir les données
        await this.fetchDemandes();
      } catch (error) {
        console.error('Erreur lors de la validation:', error);
        this.showToast('error', '❌', 'Erreur lors de la validation de la demande');
      }
    },
    async rejectRequest(req) {
      try {
        await rejeterDemande(req.id);
        const index = this.requests.findIndex(r => r.id === req.id);
        if (index !== -1) {
          this.requests[index].status = 'REJETEE';
        }
        this.activities.unshift({
          icon: 'X',
          text: `Demande ${req.reference} rejetée`,
          time: 'À l\'instant',
          type: 'error'
        });
        this.showToast('error', '❌', `Demande ${req.reference} rejetée`);
        // Rafraîchir les données
        await this.fetchDemandes();
      } catch (error) {
        console.error('Erreur lors du rejet:', error);
        this.showToast('error', '❌', 'Erreur lors du rejet de la demande');
      }
    },
    updateRequest(updatedReq) {
      const index = this.requests.findIndex(r => r.id === updatedReq.id);
      if (index !== -1) {
        this.requests[index] = { ...this.requests[index], ...updatedReq };
        this.showToast('success', '✅', 'Demande mise à jour');
      }
    },
    showToast(type, icon, message) {
      this.toast = { show: true, type, icon, message };
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    },
    showModal(title, message, onConfirm) {
      this.modal = {
        show: true,
        title,
        message,
        onConfirm
      };
    }
  },
  mounted() {
    document.addEventListener('click', (e) => {
      const notifBtn = document.querySelector('.notif-btn');
      const notifDropdown = document.querySelector('.notification-dropdown');
      if (notifBtn && notifDropdown && 
          !notifBtn.contains(e.target) && 
          !notifDropdown.contains(e.target)) {
        this.showNotifications = false;
      }
    });
  }
};
</script>
