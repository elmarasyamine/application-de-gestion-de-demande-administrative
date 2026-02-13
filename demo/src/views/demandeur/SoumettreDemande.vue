<template>
  <div class="space-y-6">
    
    <!-- HEADER SECTION -->
    <section class="relative bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-800 rounded-2xl shadow-2xl p-8 text-white overflow-hidden">
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2"></div>
      <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2"></div>
      
      <div class="relative flex items-center gap-4">
        <div class="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-sm shadow-lg transform hover:scale-110 transition-transform">
          <span v-html="getIcon('FilePlus', 32)"></span>
        </div>
        <div>
          <h2 class="text-4xl font-bold mb-1">Soumettre une demande</h2>
          <p class="text-white/90 text-lg">Remplissez le formulaire ci-dessous pour créer votre demande</p>
        </div>
      </div>
    </section>

    <!-- FORM CARD -->
    <section class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
      
      <!-- Form Header -->
      <div class="relative px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50">
        <div class="flex items-center justify-between">
          <h3 class="text-2xl font-bold text-gray-800 flex items-center gap-3">
            <span v-html="getIcon('ClipboardList', 28)" class="text-indigo-600"></span>
            <span>Informations de la demande</span>
          </h3>
          <div class="hidden md:flex items-center gap-2 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span class="text-sm font-semibold text-gray-700">Formulaire actif</span>
          </div>
        </div>
      </div>

      <!-- Form Body -->
      <form @submit.prevent="handleSubmit" class="p-8">
        <div class="space-y-8">
          
          <!-- Titre de la demande -->
          <div class="group">
            <label for="requestTitle" class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-3">
              <span v-html="getIcon('FileText', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
              <span>Titre de la demande</span>
              <span class="text-red-500">*</span>
            </label>
            <input 
              type="text"
              id="requestTitle" 
              v-model="formData.titreDemande"
              required 
              placeholder="Ex: Demande d'attestation de scolarité"
              class="w-full px-5 py-3.5 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all bg-white text-gray-900 font-medium shadow-sm hover:border-indigo-400"
            />
          </div>

          <!-- Type de demande -->
          <div class="group">
            <label for="requestType" class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-3">
              <span v-html="getIcon('ClipboardList', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
              <span>Type de demande</span>
              <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <select 
                id="requestType" 
                v-model="formData.typeDemande"
                required 
                class="w-full px-5 py-3.5 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all bg-white text-gray-900 font-medium shadow-sm hover:border-indigo-400 appearance-none cursor-pointer"
              >
                <option value="" class="text-gray-500">Sélectionnez un type de demande</option>
                <option value="Attestation de scolarité">Attestation de scolarité</option>
                <option value="Relevé de notes">Relevé de notes</option>
                <option value="Certificat de réussite">Certificat de réussite</option>
                <option value="Convention de stage">Convention de stage</option>
                <option value="Autre">Autre demande</option>
              </select>
              <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-indigo-600">
                <span v-html="getIcon('ChevronDown', 20)"></span>
              </div>
            </div>
          </div>



          <!-- Description -->
          <div class="group">
            <label for="requestDescription" class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-3">
              <span v-html="getIcon('MessageSquare', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
              <span>Description détaillée</span>
              <span class="text-gray-400 text-xs font-normal ml-1">(optionnel)</span>
            </label>
            <div class="relative">
              <textarea 
                id="requestDescription" 
                v-model="formData.description"
                @input="updateCharCount"
                maxlength="500"
                rows="6" 
                placeholder="Décrivez votre demande en détail... (Exemple: J'ai besoin d'une attestation pour mon dossier de candidature)"
                class="w-full px-5 py-4 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all resize-none shadow-sm hover:border-indigo-400 font-medium"
              ></textarea>
              <div class="absolute bottom-3 right-3 text-xs font-semibold px-3 py-1 rounded-full" :class="charCount > 450 ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-500'">
                {{ charCount }} / 500
              </div>
            </div>
          </div>

          <!-- Upload de fichier -->
          <div class="group">
            <label class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-3">
              <span v-html="getIcon('Paperclip', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
              <span>Documents justificatifs</span>
              <span class="text-gray-400 text-xs font-normal ml-1">(optionnel)</span>
            </label>
            
            <div 
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              :class="[
                'relative border-2 border-dashed rounded-2xl p-10 transition-all cursor-pointer',
                isDragging 
                  ? 'border-indigo-500 bg-indigo-50 scale-105' 
                  : 'border-gray-300 hover:border-indigo-400 hover:bg-indigo-50/30'
              ]"
            >
              <input 
                type="file" 
                id="requestDocument" 
                @change="handleFileUpload"
                accept=".pdf,.doc,.docx,.jpg,.png"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              >
              
              <div v-if="fileName === 'Aucun fichier sélectionné'" class="text-center">
                <div class="w-20 h-20 bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 rounded-3xl flex items-center justify-center mx-auto mb-5 shadow-lg transform transition-transform hover:scale-110">
                  <span v-html="getIcon('Upload', 40)" class="text-indigo-600"></span>
                </div>
                <div class="mb-3">
                  <span class="text-indigo-600 font-bold text-lg hover:underline">Cliquez pour parcourir</span>
                  <span class="text-gray-600 text-lg"> ou glissez-déposez ici</span>
                </div>
                <div class="flex items-center justify-center gap-2 flex-wrap text-sm text-gray-500">
                  <span class="px-3 py-1 bg-gray-100 rounded-full font-medium">PDF</span>
                  <span class="px-3 py-1 bg-gray-100 rounded-full font-medium">DOC</span>
                  <span class="px-3 py-1 bg-gray-100 rounded-full font-medium">DOCX</span>
                  <span class="px-3 py-1 bg-gray-100 rounded-full font-medium">JPG</span>
                  <span class="px-3 py-1 bg-gray-100 rounded-full font-medium">PNG</span>
                </div>
                <p class="text-xs text-gray-400 mt-3">Taille maximale: 5MB</p>
              </div>

              <div v-else class="text-center">
                <div class="w-20 h-20 bg-gradient-to-br from-green-100 to-emerald-100 rounded-3xl flex items-center justify-center mx-auto mb-5 shadow-lg animate-bounce">
                  <span v-html="getIcon('CheckCircle2', 40)" class="text-green-600"></span>
                </div>
                <div class="text-green-700 font-bold text-lg mb-1">Fichier ajouté !</div>
                <div class="text-gray-600 font-medium mb-4">{{ fileName }}</div>
                <button 
                  type="button"
                  @click.stop="removeFile"
                  class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-red-50 text-red-600 font-semibold hover:bg-red-100 transition-all shadow-sm hover:shadow-md"
                >
                  <span v-html="getIcon('Trash2', 18)"></span>
                  <span>Supprimer le fichier</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-4 pt-8 border-t-2 border-gray-200">
            <button 
              type="submit" 
              class="flex-1 flex items-center justify-center gap-3 px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white font-bold text-lg hover:from-indigo-700 hover:via-purple-700 hover:to-indigo-800 transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1 active:translate-y-0"
            >
              <span v-html="getIcon('Send', 24)"></span>
              <span>Soumettre la demande</span>
            </button>
            <button 
              type="button" 
              @click="resetForm"
              class="px-8 py-4 rounded-xl border-2 border-gray-300 text-gray-700 font-bold text-lg hover:bg-gray-50 hover:border-gray-400 transition-all flex items-center gap-3 shadow-md hover:shadow-lg"
            >
              <span v-html="getIcon('RotateCcw', 24)"></span>
              <span>Réinitialiser</span>
            </button>
          </div>
          
        </div>
      </form>
    </section>

  </div>
</template>

<script>
import { soumettreDemande } from '@/services/demandeService';

export default {
  name: 'SoumettreDemandeVue',
  data() {
    return {
      formData: {
        titreDemande: '',
        typeDemande: '',
        description: '',
        fichier: null
      },
      fileName: 'Aucun fichier sélectionné',
      charCount: 0,
      isDragging: false,
      isSubmitting: false,
      successMessage: '',
      errorMessage: '',
      // Bibliothèque d'icônes SVG professionnelles
      icons: {
        FilePlus: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>',
        ClipboardList: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>',
        FileText: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
        ChevronDown: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" /></svg>',
        MessageSquare: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" /></svg>',
        Paperclip: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" /></svg>',
        Upload: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" /></svg>',
        CheckCircle2: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        Trash2: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>',
        Send: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" /></svg>',
        RotateCcw: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" /></svg>'
      }
    };
  },
  methods: {
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['FileText'];
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`);
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.formData.fichier = file;
        this.fileName = file.name;
      }
    },
    handleDrop(event) {
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      if (file) {
        this.formData.fichier = file;
        this.fileName = file.name;
      }
    },
    removeFile() {
      this.formData.fichier = null;
      this.fileName = 'Aucun fichier sélectionné';
      const fileInput = document.getElementById('requestDocument');
      if (fileInput) fileInput.value = '';
    },
    async handleSubmit() {
      this.successMessage = '';
      this.errorMessage = '';
      this.isSubmitting = true;
      
      try {
        // Get user from localStorage
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          this.errorMessage = 'Vous devez être connecté pour soumettre une demande';
          this.isSubmitting = false;
          return;
        }
        const user = JSON.parse(userStr);
        
        // Prepare data matching backend DemandeDto
        const data = {
          titreDemande: this.formData.titreDemande,
          typeDemande: this.formData.typeDemande,
          idDemandeur: user.id,
          description: this.formData.description,
          fichier: this.formData.fichier
        };
        
        await soumettreDemande(data);
        
        this.successMessage = 'Votre demande a été soumise avec succès !';
        this.resetForm();
        
        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
          this.$router.push('/demandeur/tableau-de-bord');
        }, 2000);
        
      } catch (err) {
        console.error('Erreur lors de la soumission:', err);
        this.errorMessage = err.response?.data?.message || 'Erreur lors de la soumission de la demande';
      } finally {
        this.isSubmitting = false;
      }
    },
    resetForm() {
      this.formData = {
        titreDemande: '',
        typeDemande: '',
        description: '',
        fichier: null
      };
      this.fileName = 'Aucun fichier sélectionné';
      this.charCount = 0;
      const fileInput = document.getElementById('requestDocument');
      if (fileInput) fileInput.value = '';
    },
    updateCharCount(event) {
      this.charCount = event.target.value.length;
    }
  }
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.space-y-6 > section {
  animation: fadeInUp 0.5s ease-out forwards;
}
</style>