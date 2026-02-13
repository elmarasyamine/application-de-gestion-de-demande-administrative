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
          <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
            <span v-html="getIcon('ClipboardList', 24)" class="text-white"></span>
          </div>
          <transition name="fade">
            <div v-if="!sidebarCollapsed" class="flex-1">
              <h2 class="text-xl font-bold">GestionDemandes</h2>
              <p class="text-xs text-white/70">Espace Demandeur</p>
            </div>
          </transition>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-6 space-y-2 overflow-y-auto">
        <router-link 
          to="/demandeur/tableau-de-bord" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <span v-html="getIcon('LayoutDashboard', 20)"></span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Tableau de bord
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/demandeur/soumettre-demande" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <span v-html="getIcon('PlusCircle', 20)"></span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Soumettre une demande
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/demandeur/mes-demandes" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <span v-html="getIcon('FileText', 20)"></span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Mes demandes
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/demandeur/messagerie" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <span v-html="getIcon('MessageSquare', 20)"></span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Messagerie interne
            </span>
          </transition>
        </router-link>
        
        <router-link 
          to="/demandeur/profil" 
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 hover:bg-white/10 group"
          active-class="bg-white/20 shadow-lg"
        >
          <span v-html="getIcon('User', 20)"></span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="font-medium group-hover:translate-x-1 transition-transform">
              Profil
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
              <span v-html="getIcon('Menu', 24)" class="text-gray-700"></span>
            </button>
            
            <div class="relative max-w-md w-full">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" v-html="getIcon('Search', 18)"></span>
              <input 
                type="text" 
                placeholder="Rechercher..."
                v-model="globalSearch"
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
                <span v-html="getIcon('Bell', 22)" class="text-gray-700"></span>
                <span 
                  v-if="unreadNotifications > 0" 
                  class="absolute top-1 right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center"
                >
                  {{ unreadNotifications }}
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
                {{ userName.charAt(0) }}
              </div>
              <div class="hidden lg:block">
                <div class="font-semibold text-gray-800">{{ userName }}</div>
                <div class="text-xs text-gray-500">Demandeur</div>
              </div>
            </div>

            <!-- Logout Button -->
            <button 
              @click="logout"
              class="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition-colors font-medium"
            >
              <span v-html="getIcon('LogOut', 18)" class="text-red-600"></span>
              <span class="hidden md:inline">Déconnexion</span>
            </button>
          </div>
        </div>
      </header>

      <!-- ROUTER VIEW -->
      <main class="flex-1 overflow-y-auto p-6 bg-gray-50">
        <router-view 
          :requests="requests"
          :messagesData="messagesData"
          :profile="profile"
          @submit-request="submitRequest"
          @view-request="viewRequest"
          @view-all-requests="goToRequests"
          @filters-applied="showToast('info', 'Info', 'Filtres appliqués')"
          @filters-reset="showToast('info', 'Info', 'Filtres réinitialisés')"
          @edit-profile="editProfile"
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
        <span v-html="getIcon(toast.icon, 24)"></span>
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
              class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors"
            >
              <span v-html="getIcon('X', 24)"></span>
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
export default {
  name: 'HomeDemandeur',
  data() {
    return {
      sidebarCollapsed: false,
      globalSearch: '',
      userName: 'Ahmed Bennani', // Valeur par défaut, sera remplacée au mounted
      showNotifications: false,
      notifications: [
        { id: 1, text: 'Nouvelle réponse à votre demande DEM-2024-001', unread: true, time: '09:15' },
        { id: 2, text: 'Votre demande DEM-2024-002 est en cours de traitement', unread: true, time: 'Hier' },
        { id: 3, text: 'Rappel: Récupérez votre attestation au bureau', unread: true, time: '2 jours' }
      ],
      requests: [
        {
          id: 1,
          ref: 'DEM-2024-001',
          type: 'attestation',
          typeLabel: 'Attestation de scolarité',
          date: '2024-01-05',
          status: 'validee',
          statusLabel: 'Validée',
          description: 'Demande d\'attestation pour inscription au club sportif',
          history: [
            { date: '2024-01-05 10:30', status: 'Demande soumise', desc: 'Votre demande a été enregistrée' },
            { date: '2024-01-06 14:20', status: 'En cours de traitement', desc: 'Le service administratif examine votre demande' },
            { date: '2024-01-08 09:15', status: 'Validée', desc: 'Votre document est prêt' }
          ]
        },
        {
          id: 2,
          ref: 'DEM-2024-002',
          type: 'releve',
          typeLabel: 'Relevé de notes',
          date: '2024-01-10',
          status: 'en_cours',
          statusLabel: 'En cours',
          description: 'Relevé de notes semestre 1',
          history: [
            { date: '2024-01-10 11:00', status: 'Demande soumise', desc: 'Votre demande a été enregistrée' },
            { date: '2024-01-11 15:45', status: 'En cours de traitement', desc: 'Le service scolarité traite votre demande' }
          ]
        },
        {
          id: 3,
          ref: 'DEM-2024-003',
          type: 'certificat',
          typeLabel: 'Certificat de réussite',
          date: '2024-01-12',
          status: 'en_attente',
          statusLabel: 'En attente',
          description: 'Certificat de réussite année 2023',
          history: [
            { date: '2024-01-12 16:20', status: 'Demande soumise', desc: 'Votre demande a été enregistrée' }
          ]
        },
        {
          id: 4,
          ref: 'DEM-2023-156',
          type: 'stage',
          typeLabel: 'Convention de stage',
          date: '2023-12-20',
          status: 'rejetee',
          statusLabel: 'Rejetée',
          description: 'Convention de stage pour entreprise XYZ',
          history: [
            { date: '2023-12-20 10:00', status: 'Demande soumise', desc: 'Votre demande a été enregistrée' },
            { date: '2023-12-22 14:30', status: 'Rejetée', desc: 'Documents incomplets. Veuillez resoumettre.' }
          ]
        },
        {
          id: 5,
          ref: 'DEM-2024-004',
          type: 'attestation',
          typeLabel: 'Attestation de scolarité',
          date: '2024-01-15',
          status: 'en_attente',
          statusLabel: 'En attente',
          description: 'Attestation pour demande de bourse',
          history: [
            { date: '2024-01-15 09:30', status: 'Demande soumise', desc: 'Votre demande a été enregistrée' }
          ]
        }
      ],
      messagesData: [
        {
          requestId: 1,
          messages: [
            { type: 'received', text: 'Bonjour, votre demande a été validée. Vous pouvez récupérer votre document.', time: '09:15' },
            { type: 'sent', text: 'Merci beaucoup ! Où puis-je le récupérer ?', time: '09:20' },
            { type: 'received', text: 'Au bureau de la scolarité, bâtiment A, 1er étage.', time: '09:25' }
          ]
        },
        {
          requestId: 2,
          messages: [
            { type: 'received', text: 'Votre relevé de notes est en cours de préparation.', time: '15:45' },
            { type: 'sent', text: 'Combien de temps cela prendra-t-il ?', time: '16:00' },
            { type: 'received', text: 'Environ 2-3 jours ouvrables.', time: '16:15' }
          ]
        },
        {
          requestId: 4,
          messages: [
            { type: 'received', text: 'Votre demande a été rejetée car il manque des documents.', time: '14:30' },
            { type: 'sent', text: 'Quels documents manquent exactement ?', time: '15:00' },
            { type: 'received', text: 'La signature du tuteur de stage et le cachet de l\'entreprise.', time: '15:30' }
          ]
        }
      ],
      profile: {
        name: 'Ahmed Bennani',
        email: 'ahmed.bennani@example.com',
        cne: 'G123456789',
        phone: '+212 6 12 34 56 78',
        registrationDate: '15 Septembre 2023',
        level: 'Licence 3'
      },
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
      },
      // SVG Icons library
      icons: {
        ClipboardList: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>',
        LayoutDashboard: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z" /></svg>',
        PlusCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        FileText: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
        MessageSquare: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" /></svg>',
        User: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>',
        Menu: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" /></svg>',
        Search: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>',
        Bell: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>',
        LogOut: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" /></svg>',
        X: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>',
        CheckCircle2: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        XCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        Info: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" /></svg>',
        AlertCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" /></svg>'
      }
    };
  },
  computed: {
    unreadNotifications() {
      return this.notifications.filter(n => n.unread).length;
    }
  },
  methods: {
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['FileText']
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`)
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
    
    // NOUVELLE METHODE: Charger le nom depuis localStorage
    loadUserName() {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          // Essayer différentes combinaisons de champs
          if (user.prenom && user.nom) {
            this.userName = `${user.prenom} ${user.nom}`;
          } else if (user.prenom && user.name) {
            this.userName = `${user.prenom} ${user.name}`;
          } else if (user.nom) {
            this.userName = user.nom;
          } else if (user.name) {
            this.userName = user.name;
          }
          
          // Mettre à jour aussi le profile
          if (user.nom) this.profile.name = user.nom;
          if (user.prenom) this.profile.prenom = user.prenom;
          if (user.email) this.profile.email = user.email;
          if (user.cne) this.profile.cne = user.cne;
          if (user.phone || user.telephone) this.profile.phone = user.phone || user.telephone;
          
        } catch (error) {
          console.error('Erreur lors du chargement des données utilisateur:', error);
        }
      }
    },
    
    submitRequest(data) {
      const typeLabels = {
        'attestation': 'Attestation de scolarité',
        'releve': 'Relevé de notes',
        'certificat': 'Certificat de réussite',
        'stage': 'Convention de stage',
        'autre': 'Autre'
      };

      const newReq = {
        id: this.requests.length + 1,
        ref: `DEM-2024-${String(this.requests.length + 1).padStart(3, '0')}`,
        type: data.type,
        typeLabel: typeLabels[data.type],
        date: new Date().toISOString().split('T')[0],
        status: 'en_attente',
        statusLabel: 'En attente',
        description: data.description || 'Aucune description',
        history: [
          { 
            date: new Date().toLocaleString('fr-FR'), 
            status: 'Demande soumise', 
            desc: 'Votre demande a été enregistrée' 
          }
        ]
      };

      this.requests.unshift(newReq);
      this.showToast('success', 'CheckCircle2', 'Demande soumise avec succès !');
      
      setTimeout(() => {
        this.$router.push('/demandeur/mes-demandes');
      }, 1500);
    },
    viewRequest(id) {
      this.$router.push(`/demandeur/demande/${id}`);
    },
    goToRequests() {
      this.$router.push('/demandeur/mes-demandes');
    },
    editProfile() {
      this.showToast('info', 'Info', 'Fonctionnalité en développement');
    },
    logout() {
      this.showModal(
        'Déconnexion',
        'Êtes-vous sûr de vouloir vous déconnecter ?',
        () => {
          this.showToast('info', 'Info', 'Déconnexion en cours...');
          setTimeout(() => {
            localStorage.removeItem('userToken');
            localStorage.removeItem('userRole');
            localStorage.removeItem('user'); // Nettoyer aussi les données utilisateur
            this.$router.push('/login');
          }, 1000);
        }
      );
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
        onConfirm: () => {
          onConfirm();
          this.modal.show = false;
        }
      };
    }
  },
  mounted() {
    // MODIFICATION: Charger le nom au démarrage
    this.loadUserName();
    
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

<style scoped>
/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.dropdown-enter-active, .dropdown-leave-active {
  transition: all 0.3s ease;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from > div, .modal-leave-to > div {
  transform: scale(0.9);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #c7d2fe;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a5b4fc;
}
</style>