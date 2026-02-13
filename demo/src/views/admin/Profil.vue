<template>
  <div class="space-y-8">
    
    <!-- PROFILE HEADER SECTION -->
    <section class="relative">
      
      <!-- Main Profile Card -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 overflow-hidden">
        
        <!-- Cover Background -->
        <div class="relative h-48 overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br from-indigo-600 via-violet-600 to-purple-600"></div>
          <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIgZmlsbD0id2hpdGUiIGZpbGwtb3BhY2l0eT0iMC4xIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] opacity-40"></div>
        </div>

        <!-- Profile Content -->
        <div class="relative px-8 pb-8">
          <!-- Avatar -->
          <div class="flex flex-col items-center -mt-20 mb-6">
            <div class="relative group">
              <div class="w-36 h-36 rounded-3xl bg-gradient-to-br from-white to-indigo-50 flex items-center justify-center text-6xl font-black text-indigo-600 shadow-2xl border-8 border-white group-hover:scale-105 transition-transform duration-300 uppercase">
                {{ admin.nom ? admin.nom.charAt(0) : 'A' }}
              </div>
              <div class="absolute -bottom-2 -right-2 w-12 h-12 bg-gradient-to-br from-emerald-400 to-green-500 rounded-2xl flex items-center justify-center shadow-lg border-4 border-white">
                <Check class="w-6 h-6 text-white" />
              </div>
            </div>
          </div>

          <!-- Profile Info -->
          <div class="text-center mb-6">
            <h2 class="text-3xl font-black text-slate-800 mb-2">{{ admin.prenom }} {{ admin.nom }}</h2>
            <p class="text-slate-600 font-semibold mb-3 flex items-center justify-center gap-2">
              <span class="text-2xl">📧</span>
              <span>{{ admin.email }}</span>
            </p>
            <div class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-bold shadow-lg shadow-indigo-500/30">
              <span class="text-lg">🛡️</span>
              <span>Administrateur</span>
            </div>
          </div>

          <!-- Edit Profile Button -->
          <div class="flex justify-center">
            <button 
              @click="openEditModal"
              class="group flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-slate-100 to-slate-200 hover:from-indigo-600 hover:to-violet-600 border-2 border-slate-200 hover:border-transparent text-slate-700 hover:text-white font-bold transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl hover:shadow-indigo-500/30"
            >
              <span class="text-xl">✏️</span>
              <span>Modifier le profil</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- INFO & SECURITY GRID -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- ACCOUNT INFO CARD -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 overflow-hidden">
        <div class="px-6 py-5 border-b-2 border-slate-100 bg-gradient-to-r from-slate-50 to-blue-50">
          <h3 class="text-xl font-bold text-slate-800 flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-md">
              <FileText class="w-5 h-5" />
            </div>
            <span>Informations du compte</span>
          </h3>
        </div>

        <div class="p-6 space-y-2">
          <!-- Name -->
          <div class="group flex items-start gap-4 p-4 rounded-2xl hover:bg-slate-50 transition-all cursor-pointer">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center text-2xl flex-shrink-0">
              👤
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Nom complet</div>
              <div class="text-base font-bold text-slate-800">{{ admin.prenom }} {{ admin.nom }}</div>
            </div>
          </div>

          <!-- Email -->
          <div class="group flex items-start gap-4 p-4 rounded-2xl hover:bg-slate-50 transition-all cursor-pointer">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-100 to-green-100 flex items-center justify-center text-2xl flex-shrink-0">
              📧
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Email</div>
              <div class="text-base font-bold text-slate-800 flex items-center gap-2">
                <span>{{ admin.email }}</span>
                <span class="px-2 py-0.5 rounded-full bg-green-100 text-green-700 text-xs font-bold">Vérifié</span>
              </div>
            </div>
          </div>

          <!-- CNI -->
          <div class="group flex items-start gap-4 p-4 rounded-2xl hover:bg-slate-50 transition-all cursor-pointer">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center text-2xl flex-shrink-0">
              🆔
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">CNI</div>
              <div class="text-base font-bold text-slate-800">{{ admin.cni || 'Non renseigné' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- SECURITY CARD -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 overflow-hidden">
        <div class="px-6 py-5 border-b-2 border-slate-100 bg-gradient-to-r from-slate-50 to-red-50">
          <h3 class="text-xl font-bold text-slate-800 flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-red-500 to-rose-600 flex items-center justify-center text-white shadow-md">
              <span class="text-lg">🔒</span>
            </div>
            <span>Sécurité</span>
          </h3>
        </div>

        <div class="p-6 space-y-2">
          <!-- Password -->
          <div 
            @click="openPasswordModal"
            class="group flex items-start gap-4 p-4 rounded-2xl hover:bg-slate-50 transition-all cursor-pointer border-2 border-transparent hover:border-indigo-200"
          >
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-100 to-violet-100 flex items-center justify-center text-2xl flex-shrink-0 group-hover:scale-110 transition-transform">
              🔐
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Mot de passe</div>
              <div class="text-base font-bold text-slate-800">••••••••</div>
              <div class="text-xs text-indigo-600 font-semibold mt-1">Cliquer pour modifier</div>
            </div>
            <div class="text-indigo-600 group-hover:translate-x-1 transition-transform">
              <span class="text-xl">✏️</span>
            </div>
          </div>
        </div>
      </div>

    </section>

    <!-- MODAL EDIT PROFILE -->
    <div v-if="modals.editProfile" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
       <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg p-8 transform transition-all">
          <h3 class="text-2xl font-bold mb-6 text-gray-800">Modifier le profil</h3>
          <div class="space-y-4">
             <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Nom</label>
                <input v-model="form.nom" type="text" class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
             </div>
             <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Prénom</label>
                <input v-model="form.prenom" type="text" class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
             </div>
             <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Email</label>
                <input v-model="form.email" type="email" class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
             </div>
             <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">CNI</label>
                <input v-model="form.cni" type="text" class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
             </div>
          </div>
          <div class="flex justify-end gap-3 mt-8">
             <button @click="modals.editProfile = false" class="px-6 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold">Annuler</button>
             <button @click="updateProfile" class="px-6 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold">Enregistrer</button>
          </div>
       </div>
    </div>

    <!-- MODAL CHANGE PASSWORD -->
    <div v-if="modals.changePassword" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
       <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8 transform transition-all">
          <h3 class="text-2xl font-bold mb-6 text-gray-800">Changer mot de passe</h3>
          <div class="space-y-4">
             <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Nouveau mot de passe</label>
                <input v-model="pwdForm.newPassword" type="password" class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
             </div>
             <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Confirmer</label>
                <input v-model="pwdForm.confirmPassword" type="password" class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-500" />
             </div>
          </div>
          <div class="flex justify-end gap-3 mt-8">
             <button @click="modals.changePassword = false" class="px-6 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold">Annuler</button>
             <button @click="updatePwd" class="px-6 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold">Changer</button>
          </div>
       </div>
    </div>

  </div>
</template>

<script>
import { FileText, Shield, AlertTriangle, Check } from 'lucide-vue-next';
import { getAdministrateurById, updateAdministrateur, updatePassword } from '../../services/adminService';

export default {
  name: 'Profil',
  components: { FileText, Shield, AlertTriangle, Check },
  data() {
    return {
      alert: null, // For notifications if needed, or use Toast from layout
      admin: {},
      modals: {
        editProfile: false,
        changePassword: false
      },
      form: {
        nom: '',
        prenom: '',
        email: '',
        cni: ''
      },
      pwdForm: {
        newPassword: '',
        confirmPassword: ''
      }
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        if(user && user.id) {
            try {
                const res = await getAdministrateurById(user.id);
                this.admin = res.data;
            } catch (e) {
                console.error("Erreur fetch admin", e);
            }
        }
    },
    openEditModal() {
        this.form = { ...this.admin };
        this.modals.editProfile = true;
    },
    openPasswordModal() {
        this.pwdForm = { newPassword: '', confirmPassword: '' };
        this.modals.changePassword = true;
    },
    async updateProfile() {
        if (!this.form.nom || !this.form.prenom || !this.form.email) {
            alert("Veuillez remplir les champs obligatoires");
            return;
        }
        try {
            await updateAdministrateur(this.admin.id, this.form);
            this.modals.editProfile = false;
            await this.fetchData();
            // Update LocalStorage to reflect changes immediately in other components
            const lsUser = JSON.parse(localStorage.getItem('user') || '{}');
            const updated = { ...lsUser, ...this.form };
            localStorage.setItem('user', JSON.stringify(updated));
            alert("Profil mis à jour avec succès !");
            // Reload page to refresh Layout header if needed, or use Bus
            window.location.reload(); 
        } catch (e) {
            console.error(e);
            alert("Erreur lors de la mise à jour");
        }
    },
    async updatePwd() {
        if (this.pwdForm.newPassword !== this.pwdForm.confirmPassword) {
            alert("Les mots de passe ne correspondent pas");
            return;
        }
        if (this.pwdForm.newPassword.length < 4) {
             alert("Mot de passe trop court");
             return;
        }
        try {
            await updatePassword(this.admin.id, this.pwdForm.newPassword);
            this.modals.changePassword = false;
            alert("Mot de passe modifié avec succès !");
        } catch(e) {
            console.error(e);
            alert("Erreur lors du changement de mot de passe");
        }
    }
  }
};
</script>

<style scoped>
/* Animations and existing styles managed by Tailwind mainly, keeping minimal custom css */
.profil-admin {
  animation: fadeInUp 0.6s ease;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>