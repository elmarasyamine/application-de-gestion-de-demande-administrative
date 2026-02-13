<template>
  <div class="space-y-6">
    
    <!-- PROFILE SECTION -->
    <section class="space-y-6">
      
      <!-- PROFILE CARD -->
      <div class="relative bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <!-- Header Background -->
        <div class="h-40 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-800 relative">
          <!-- Decorative circles -->
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2"></div>
          <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2"></div>
        </div>
        
        <!-- Profile Content -->
        <div class="relative px-8 pb-8">
          <!-- Avatar -->
          <div class="absolute -top-16 left-8">
            <div class="w-32 h-32 bg-gradient-to-br from-indigo-400 to-purple-600 rounded-3xl flex items-center justify-center text-white font-bold text-5xl shadow-2xl border-4 border-white">
              {{ initials }}
            </div>
          </div>
          
          <!-- Profile Info -->
          <div class="pt-20">
            <h2 class="text-3xl font-bold text-gray-800 mb-2">{{ fullName }}</h2>
            <p class="text-lg text-gray-600 mb-6 flex items-center gap-2">
              <span v-html="getIcon('Mail', 20)" class="text-indigo-600"></span>
              {{ profile.email }}
            </p>
            
            <button 
              @click="$emit('edit-profile')"
              class="flex items-center gap-3 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <span v-html="getIcon('Edit', 20)"></span>
              <span>Modifier le profil</span>
            </button>
          </div>
        </div>
      </div>

      <!-- INFO CARD -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <!-- Card Header -->
        <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50">
          <h3 class="text-2xl font-bold text-gray-800 flex items-center gap-3">
            <span v-html="getIcon('UserCircle', 28)" class="text-indigo-600"></span>
            <span>Informations personnelles</span>
          </h3>
        </div>
        
        <!-- Info List -->
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- CNI -->
          <div class="flex items-start gap-4 p-5 rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 hover:shadow-md transition-all">
            <div class="w-14 h-14 bg-blue-500 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md text-white">
              <span v-html="getIcon('IdCard', 28)"></span>
            </div>
            <div class="flex-1">
              <div class="text-sm font-bold text-gray-600 mb-1">CNI</div>
              <div class="text-lg font-bold text-gray-800">{{ profile.cni || 'Non renseigné' }}</div>
            </div>
          </div>

          <!-- Type de compte -->
          <div class="flex items-start gap-4 p-5 rounded-xl bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 hover:shadow-md transition-all">
            <div class="w-14 h-14 bg-green-500 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md text-white">
              <span v-html="getIcon('User', 28)"></span>
            </div>
            <div class="flex-1">
              <div class="text-sm font-bold text-gray-600 mb-1">Type de compte</div>
              <div class="text-lg font-bold text-gray-800">{{ profile.type || 'Demandeur' }}</div>
            </div>
          </div>

          <!-- Nom -->
          <div class="flex items-start gap-4 p-5 rounded-xl bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 hover:shadow-md transition-all">
            <div class="w-14 h-14 bg-purple-500 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md text-white">
              <span v-html="getIcon('UserCircle', 28)"></span>
            </div>
            <div class="flex-1">
              <div class="text-sm font-bold text-gray-600 mb-1">Nom</div>
              <div class="text-lg font-bold text-gray-800">{{ profile.name || 'Non renseigné' }}</div>
            </div>
          </div>

          <!-- Prénom -->
          <div class="flex items-start gap-4 p-5 rounded-xl bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-200 hover:shadow-md transition-all">
            <div class="w-14 h-14 bg-orange-500 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md text-white">
              <span v-html="getIcon('UserCircle', 28)"></span>
            </div>
            <div class="flex-1">
              <div class="text-sm font-bold text-gray-600 mb-1">Prénom</div>
              <div class="text-lg font-bold text-gray-800">{{ profile.prenom || 'Non renseigné' }}</div>
            </div>
          </div>

        </div>
      </div>

    </section>
  </div>
</template>

<script>
export default {
  name: 'ProfilVue',
  data() {
    return {
      profile: {
        name: '',
        prenom: '',
        email: '',
        cni: '',
        type: ''
      },
      loading: true,
      // Bibliothèque d'icônes SVG
      icons: {
        Mail: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" /></svg>',
        Edit: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" /></svg>',
        UserCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" /></svg>',
        Award: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 002.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 012.916.52 6.003 6.003 0 01-5.395 4.972m0 0a6.726 6.726 0 01-2.749 1.35m0 0a6.772 6.772 0 01-3.044 0" /></svg>',
        Phone: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" /></svg>',
        Calendar: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>',
        BookOpen: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>',
        User: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>',
        IdCard: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" /></svg>'
      }
    };
  },
  computed: {
    fullName() {
      return `${this.profile.prenom || ''} ${this.profile.name || ''}`.trim() || 'Utilisateur';
    },
    initials() {
      const first = this.profile.prenom?.charAt(0) || '';
      const last = this.profile.name?.charAt(0) || '';
      return (first + last).toUpperCase() || 'U';
    }
  },
  methods: {
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['User'];
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`);
    },
    loadProfile() {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        this.profile = {
          name: user.nom || '',
          prenom: user.prenom || '',
          email: user.email || '',
          cni: user.cni || '',
          type: user.type || 'Demandeur'
        };
      }
      this.loading = false;
    }
  },
  mounted() {
    this.loadProfile();
  }
};
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.space-y-6 {
  animation: fadeInUp 0.6s ease;
}

/* Smooth hover effects */
.flex.items-start.gap-4 {
  transition: all 0.3s ease;
}

.flex.items-start.gap-4:hover {
  transform: translateX(5px);
}

/* Responsive avatar */
@media (max-width: 768px) {
  .absolute.-top-16 {
    position: static;
    margin: -4rem auto 1rem;
  }
  
  .pt-20 {
    padding-top: 1rem;
    text-align: center;
  }
  
  .pt-20 p {
    justify-content: center;
  }
  
  .pt-20 button {
    margin: 0 auto;
  }
}

/* Card animations */
.bg-white.rounded-2xl {
  animation: fadeInUp 0.6s ease;
}

/* Info card hover effect */
.p-6.grid > div:hover {
  transform: scale(1.02);
}
</style>