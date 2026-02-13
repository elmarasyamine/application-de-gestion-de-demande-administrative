<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <!-- Header -->
    <!-- Header -->
    <div class="mb-6 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
      <button 
        @click="$router.push('/admin/demandes')"
        class="flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-gray-200 text-gray-700 font-medium hover:bg-gray-50 transition-all shadow-sm w-fit"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Retour aux demandes
      </button>

      <div v-if="demande" class="flex flex-wrap items-center gap-3">
        <!-- Actions Rapides Header -->
        <button 
          v-if="demande.status === 'SOUMISE' || demande.status === 'EN_TRAITEMENT'"
          @click="valider"
          :disabled="actionLoading"
          class="flex items-center gap-2 px-4 py-2 rounded-xl bg-green-600 text-white font-medium hover:bg-green-700 transition-all shadow-md"
        >
          <span v-if="actionLoading" class="animate-spin">⏳</span>
          <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          Valider
        </button>

        <button 
          v-if="demande.status === 'SOUMISE' || demande.status === 'EN_TRAITEMENT'"
          @click="rejeter"
          :disabled="actionLoading"
          class="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-600 text-white font-medium hover:bg-red-700 transition-all shadow-md"
        >
          <span v-if="actionLoading" class="animate-spin">⏳</span>
          <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          Rejeter
        </button>

        <button 
          @click="downloadPDF"
          class="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition-all shadow-md"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Télécharger PDF
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-2xl p-8 text-center">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-xl font-bold text-red-700 mb-2">Erreur</h2>
      <p class="text-red-600">{{ error }}</p>
      <button 
        @click="fetchDemande"
        class="mt-4 px-6 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors"
      >
        Réessayer
      </button>
    </div>

    <!-- Content -->
    <div v-else-if="demande" class="space-y-6">
      <!-- Title Card -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-indigo-200 text-sm font-medium mb-1">Demande</p>
              <h1 class="text-2xl font-bold text-white">{{ demande.reference || `REQ${String(demande.id).padStart(3, '0')}` }}</h1>
            </div>
            <span 
              :class="[
                'px-4 py-2 rounded-xl text-sm font-bold uppercase',
                statusClasses[demande.status] || 'bg-gray-100 text-gray-700'
              ]"
            >
              {{ statusLabels[demande.status] || demande.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Info Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Demande Info -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <span class="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center text-indigo-600">📋</span>
            Informations de la demande
          </h2>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center py-3 border-b border-gray-100">
              <span class="text-gray-500 font-medium">Titre</span>
              <span class="text-gray-800 font-semibold">{{ demande.titreDemande || 'Non spécifié' }}</span>
            </div>
            <div class="flex justify-between items-center py-3 border-b border-gray-100">
              <span class="text-gray-500 font-medium">Type</span>
              <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                {{ demande.typeDemande || 'Non spécifié' }}
              </span>
            </div>
            <div class="flex justify-between items-center py-3 border-b border-gray-100">
              <span class="text-gray-500 font-medium">Date de dépôt</span>
              <span class="text-gray-800 font-semibold">{{ formatDate(demande.dateDepot) }}</span>
            </div>
            <div class="flex justify-between items-center py-3 border-b border-gray-100">
              <span class="text-gray-500 font-medium">Référence</span>
              <span class="font-mono text-indigo-600 font-bold">{{ demande.reference || `REQ${String(demande.id).padStart(3, '0')}` }}</span>
            </div>
          </div>
        </div>

        <!-- Demandeur Info -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <span class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center text-green-600">👤</span>
            Informations du demandeur
          </h2>
          
          <div v-if="demande.demandeur" class="space-y-4">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                {{ getInitials(demande.demandeur) }}
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-800">
                  {{ demande.demandeur.prenom }} {{ demande.demandeur.nom }}
                </h3>
                <p class="text-gray-500">{{ demande.demandeur.email }}</p>
              </div>
            </div>
            
            <div class="flex justify-between items-center py-3 border-b border-gray-100">
              <span class="text-gray-500 font-medium">CNI</span>
              <span class="text-gray-800 font-semibold">{{ demande.demandeur.cni || 'Non renseigné' }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <span class="text-4xl mb-2 block">👤</span>
            Informations du demandeur non disponibles
          </div>
        </div>
      </div>

      <!-- Fichier Joint Section -->
      <div v-if="demande.nomFichier" class="bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600">📎</span>
          Fichier joint
        </h2>
        
        <div class="border-2 border-dashed border-gray-200 rounded-xl p-6 bg-gray-50">
          <!-- Si c'est une image -->
          <div v-if="isImage(demande.nomFichier)" class="space-y-4">
            <div class="relative group cursor-pointer" @click="openFileModal">
              <img 
                :src="getFileUrl(demande.nomFichier)" 
                :alt="demande.nomFichier"
                class="max-h-64 mx-auto rounded-xl shadow-md object-contain hover:shadow-xl transition-all"
                @error="handleImageError"
              />
              <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 rounded-xl flex items-center justify-center transition-all">
                <span class="text-white opacity-0 group-hover:opacity-100 font-semibold flex items-center gap-2">
                  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                  </svg>
                  Voir en grand
                </span>
              </div>
            </div>
          </div>
          
          <!-- Si c'est un autre type de fichier -->
          <div v-else class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white text-xl shadow-md">
                {{ getFileIcon(demande.nomFichier) }}
              </div>
              <div>
                <p class="font-semibold text-gray-800">{{ demande.nomFichier }}</p>
                <p class="text-sm text-gray-500">{{ getFileType(demande.nomFichier) }}</p>
              </div>
            </div>
            <div class="flex gap-3">
              <a 
                :href="getFileUrl(demande.nomFichier)" 
                target="_blank"
                class="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-xl font-medium hover:bg-indigo-200 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                Ouvrir
              </a>
              <a 
                :href="getFileUrl(demande.nomFichier)" 
                download
                class="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-xl font-medium hover:bg-green-200 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Télécharger
              </a>
            </div>
          </div>
          
          <!-- Boutons pour les images -->
          <div v-if="isImage(demande.nomFichier)" class="flex justify-center gap-4 mt-4 pt-4 border-t border-gray-200">
            <button
              @click="openFileModal"
              class="flex items-center gap-2 px-6 py-2 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 transition-colors shadow-md"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
              </svg>
              Voir en grand
            </button>
            <a 
              :href="getFileUrl(demande.nomFichier)" 
              download
              class="flex items-center gap-2 px-6 py-2 bg-green-600 text-white rounded-xl font-medium hover:bg-green-700 transition-colors shadow-md"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Télécharger
            </a>
          </div>
        </div>
      </div>

      <!-- Description -->
      <div class="bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
          <span class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600">📝</span>
          Description de la demande
        </h2>
        <div class="bg-gray-50 rounded-xl p-6 text-gray-700 leading-relaxed">
          {{ demande.description || 'Aucune description fournie.' }}
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center text-orange-600">⚡</span>
          Actions
        </h2>
        
        <div class="flex flex-wrap gap-4">
          <button 
            v-if="demande.status === 'SOUMISE' || demande.status === 'EN_TRAITEMENT'"
            @click="valider"
            :disabled="actionLoading"
            class="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition-all shadow-md hover:shadow-lg disabled:opacity-50"
          >
            <span v-if="actionLoading" class="animate-spin">⏳</span>
            <span v-else>✅</span>
            Valider la demande
          </button>
          
          <button 
            v-if="demande.status === 'SOUMISE' || demande.status === 'EN_TRAITEMENT'"
            @click="rejeter"
            :disabled="actionLoading"
            class="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-xl font-semibold hover:bg-red-700 transition-all shadow-md hover:shadow-lg disabled:opacity-50"
          >
            <span v-if="actionLoading" class="animate-spin">⏳</span>
            <span v-else>❌</span>
            Rejeter la demande
          </button>



          <button 
            @click="$router.push('/admin/messagerie')"
            class="flex items-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-semibold hover:bg-gray-200 transition-all"
          >
            💬 Contacter le demandeur
          </button>
        </div>

        <!-- Status Info -->
        <div v-if="demande.status !== 'SOUMISE' && demande.status !== 'EN_TRAITEMENT'" class="mt-6 p-4 rounded-xl bg-gray-50 border border-gray-200">
          <p class="text-gray-600">
            <span class="font-semibold">Statut actuel :</span> 
            Cette demande a été 
            <span :class="demande.status === 'VALIDEE' || demande.status === 'TRAITEE' ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'">
              {{ statusLabels[demande.status] || demande.status }}
            </span>
          </p>
        </div>
      </div>
    </div>

    <!-- File Modal -->
    <transition name="modal">
      <div 
        v-if="showFileModal" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-80"
        @click="closeFileModal"
      >
        <div class="relative max-w-5xl max-h-full" @click.stop>
          <button 
            @click="closeFileModal"
            class="absolute -top-4 -right-4 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center text-gray-600 hover:text-gray-900 hover:scale-110 transition-all z-10"
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <img 
            v-if="demande && demande.nomFichier"
            :src="getFileUrl(demande.nomFichier)" 
            :alt="demande.nomFichier"
            class="max-w-full max-h-[85vh] rounded-2xl shadow-2xl object-contain"
          />
          <div class="mt-4 text-center">
            <a 
              :href="getFileUrl(demande.nomFichier)" 
              download
              class="inline-flex items-center gap-2 px-6 py-3 bg-white text-gray-800 rounded-xl font-semibold hover:bg-gray-100 transition-colors shadow-lg"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Télécharger l'image
            </a>
          </div>
        </div>
      </div>
    </transition>

    <!-- Toast -->
    <transition name="toast">
      <div 
        v-if="toast.show"
        :class="[
          'fixed bottom-6 right-6 px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 z-50',
          toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        ]"
      >
        <span class="text-2xl">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
        <span class="font-medium">{{ toast.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script>
import { getDemandeById, validerDemande, rejeterDemande, traiterDemande } from '../../services/demandeService';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export default {
  name: 'DetailDemandeAdmin',
  data() {
    return {
      demande: null,
      loading: true,
      error: null,
      actionLoading: false,
      showFileModal: false,
      toast: {
        show: false,
        type: '',
        message: ''
      },
      statusLabels: {
        'SOUMISE': 'Soumise',
        'EN_TRAITEMENT': 'En traitement',
        'VALIDEE': 'Validée',
        'REJETEE': 'Rejetée',
        'TRAITEE': 'Traitée'
      },
      statusClasses: {
        'SOUMISE': 'bg-yellow-100 text-yellow-800',
        'EN_TRAITEMENT': 'bg-blue-100 text-blue-800',
        'VALIDEE': 'bg-green-100 text-green-800',
        'REJETEE': 'bg-red-100 text-red-800',
        'TRAITEE': 'bg-indigo-100 text-indigo-800'
      }
    };
  },
  async created() {
    await this.fetchDemande();
  },
  methods: {
    async fetchDemande() {
      this.loading = true;
      this.error = null;
      
      try {
        const id = this.$route.params.id;
        const response = await getDemandeById(id);
        this.demande = response.data;
      } catch (err) {
        console.error('Erreur lors du chargement:', err);
        this.error = 'Impossible de charger les détails de la demande.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'Non spécifié';
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch {
        return dateString;
      }
    },
    getInitials(user) {
      if (!user) return '?';
      const prenom = user.prenom || '';
      const nom = user.nom || '';
      return `${prenom.charAt(0)}${nom.charAt(0)}`.toUpperCase();
    },
    getFileUrl(filename) {
      return `http://localhost:8093/uploads/${filename}`;
    },
    isImage(filename) {
      if (!filename) return false;
      const ext = filename.split('.').pop().toLowerCase();
      return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'].includes(ext);
    },
    getFileIcon(filename) {
      if (!filename) return '📄';
      const ext = filename.split('.').pop().toLowerCase();
      const icons = {
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'xls': '📗',
        'xlsx': '📗',
        'txt': '📝',
        'zip': '📦',
        'rar': '📦'
      };
      return icons[ext] || '📄';
    },
    getFileType(filename) {
      if (!filename) return 'Fichier';
      const ext = filename.split('.').pop().toLowerCase();
      const types = {
        'pdf': 'Document PDF',
        'doc': 'Document Word',
        'docx': 'Document Word',
        'xls': 'Fichier Excel',
        'xlsx': 'Fichier Excel',
        'txt': 'Fichier texte',
        'zip': 'Archive ZIP',
        'rar': 'Archive RAR',
        'jpg': 'Image JPEG',
        'jpeg': 'Image JPEG',
        'png': 'Image PNG',
        'gif': 'Image GIF'
      };
      return types[ext] || `Fichier ${ext.toUpperCase()}`;
    },
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="150" viewBox="0 0 200 150"><rect fill="%23f3f4f6" width="200" height="150"/><text fill="%239ca3af" font-family="Arial" font-size="14" x="50%" y="50%" text-anchor="middle" dy=".3em">Image non disponible</text></svg>';
    },
    openFileModal() {
      this.showFileModal = true;
      document.body.style.overflow = 'hidden';
    },
    closeFileModal() {
      this.showFileModal = false;
      document.body.style.overflow = '';
    },
    async valider() {
      this.actionLoading = true;
      try {
        await validerDemande(this.demande.id);
        this.demande.status = 'VALIDEE';
        this.showToast('success', 'Demande validée avec succès !');
      } catch (err) {
        console.error('Erreur:', err);
        this.showToast('error', 'Erreur lors de la validation');
      } finally {
        this.actionLoading = false;
      }
    },
    async rejeter() {
      this.actionLoading = true;
      try {
        await rejeterDemande(this.demande.id);
        this.demande.status = 'REJETEE';
        this.showToast('success', 'Demande rejetée');
      } catch (err) {
        console.error('Erreur:', err);
        this.showToast('error', 'Erreur lors du rejet');
      } finally {
        this.actionLoading = false;
      }
    },

    downloadPDF() {
      const doc = new jsPDF();
      
      // Header
      doc.setFontSize(22);
      doc.setTextColor(79, 70, 229); // Indigo 600
      doc.text("Détails de la Demande", 105, 20, { align: "center" });
      
      doc.setFontSize(12);
      doc.setTextColor(100);
      doc.text(`Réf: ${this.demande.reference || this.demande.id}`, 105, 30, { align: "center" });

      // Info Demande
      doc.autoTable({
        startY: 40,
        head: [['Information', 'Détail']],
        body: [
          ['Titre', this.demande.titreDemande || '-'],
          ['Type', this.demande.typeDemande || '-'],
          ['Date de dépôt', this.formatDate(this.demande.dateDepot)],
          ['Statut', this.statusLabels[this.demande.status] || this.demande.status],
        ],
        theme: 'grid',
        headStyles: { fillColor: [79, 70, 229] }
      });

      // Info Demandeur
      doc.text("Informations Demandeur", 14, doc.lastAutoTable.finalY + 15);
      
      const demandeur = this.demande.demandeur || {};
      doc.autoTable({
        startY: doc.lastAutoTable.finalY + 20,
        body: [
          ['Nom complet', `${demandeur.prenom || ''} ${demandeur.nom || ''}`],
          ['Email', demandeur.email || '-'],
          ['CNI', demandeur.cni || '-']
        ],
        theme: 'striped',
        showHead: 'never'
      });

      // Description
      doc.text("Description", 14, doc.lastAutoTable.finalY + 15);
      doc.setFontSize(10);
      doc.setTextColor(50);
      
      const splitDescription = doc.splitTextToSize(this.demande.description || 'Aucune description', 180);
      doc.text(splitDescription, 14, doc.lastAutoTable.finalY + 22);

      // Save
      doc.save(`Demande_${this.demande.reference || this.demande.id}.pdf`);
    },
    showToast(type, message) {
      this.toast = { show: true, type, message };
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    }
  }
};
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.9);
}
</style>

