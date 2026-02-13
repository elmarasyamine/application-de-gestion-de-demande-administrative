<template>
  <div class="space-y-6">
    
    <!-- FILTERS SECTION -->
    <section class="bg-white rounded-2xl shadow-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        
        <!-- Statut Filter -->
        <div>
          <label class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
            <Tag class="w-5 h-5" />
            <span>Statut</span>
          </label>
            <select 
            v-model="filters.status" 
            class="w-full px-4 py-2.5 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition bg-white"
          >
            <option value="">Tous les statuts</option>
            <option value="SOUMISE">En attente</option>
            <option value="EN_TRAITEMENT">En traitement</option>
            <option value="VALIDEE">Validée</option>
            <option value="REJETEE">Rejetée</option>
            <option value="TRAITEE">Traitée</option>
          </select>
        </div>

        <!-- Type Filter -->
        <div>
          <label class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
            <FileText class="w-5 h-5" />
            <span>Type</span>
          </label>
          <select 
            v-model="filters.type" 
            class="w-full px-4 py-2.5 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition bg-white"
          >
            <option value="">Tous les types</option>
            <option value="Attestation de scolarité">Attestation de scolarité</option>
            <option value="Relevé de notes">Relevé de notes</option>
            <option value="Certificat de réussite">Certificat de réussite</option>
            <option value="Convention de stage">Convention de stage</option>
            <option value="Autre">Autre</option>
          </select>
        </div>

        <!-- Date Filter -->
        <div>
          <label class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
            <Calendar class="w-5 h-5" />
            <span>Date</span>
          </label>
          <input 
            type="date" 
            v-model="filters.date" 
            class="w-full px-4 py-2.5 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
          >
        </div>
        
        <!-- Search Filter -->
         <div class="col-span-full md:col-span-1">
          <label class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
            <Search class="w-5 h-5" />
            <span>Recherche</span>
          </label>
          <input 
            type="text" 
            v-model="filters.search" 
            placeholder="Nom, référence..."
            class="w-full px-4 py-2.5 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
          >
        </div>

        <!-- Action Buttons -->
        <div class="flex items-end gap-2">
          <button 
            @click="applyFilters"
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition-colors shadow-md hover:shadow-lg"
          >
            <Search class="w-5 h-5" />
            <span class="hidden sm:inline">Filtrer</span>
          </button>
          <button 
            @click="resetFilters"
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gray-100 text-gray-700 font-semibold hover:bg-gray-200 transition-colors"
          >
            <RotateCcw class="w-5 h-5" />
            <span class="hidden sm:inline">Reset</span>
          </button>
        </div>
      </div>
    </section>

    <!-- TABLE SECTION -->
    <section class="bg-white rounded-2xl shadow-lg overflow-hidden">
      
      <!-- Table Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-indigo-50 to-purple-50">
        <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
          <FileText class="w-6 h-6 text-indigo-600" />
          <span>Toutes les demandes</span>
        </h3>
        <div class="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm border border-gray-100">
          <span class="text-lg font-bold text-indigo-600">{{ filteredRequests.length }}</span>
          <span class="text-sm text-gray-600 font-medium">demande(s)</span>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Référence
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Nom
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Date
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Statut
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="req in filteredRequests" 
              :key="req.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <!-- Référence -->
              <td class="px-6 py-4">
                <span class="font-mono text-sm font-semibold text-indigo-600">
                  {{ req.reference }}
                </span>
              </td>
              
              <!-- Nom -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-400 to-purple-600 flex items-center justify-center text-white font-bold shadow-md">
                    {{ (req.demandeur && req.demandeur.nom) ? req.demandeur.nom.charAt(0) : '?' }}
                  </div>
                  <div class="flex flex-col">
                     <span class="font-medium text-gray-800">{{ req.demandeur ? req.demandeur.nom + ' ' + req.demandeur.prenom : 'Inconnu' }}</span>
                     <span class="text-xs text-gray-500">{{ req.demandeur ? req.demandeur.email : '' }}</span>
                  </div>
                </div>
              </td>
              
              <!-- Type -->
              <td class="px-6 py-4">
                <span class="text-gray-700 font-medium">{{ req.typeDemande }}</span>
              </td>
              
              <!-- Date -->
              <td class="px-6 py-4">
                <span class="text-gray-600 text-sm">{{ formatDate(req.dateDepot) }}</span>
              </td>
              
              <!-- Statut -->
              <td class="px-6 py-4">
                <span 
                  :class="[
                    'inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold',
                    getStatusClass(req.status)
                  ]"
                >
                  <!-- Icon placeholder could go here like dashboard -->
                  {{ getStatusLabel(req.status) }}
                </span>
              </td>
              
              <!-- Actions -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <button 
                    @click="viewRequest(req)"
                    class="w-8 h-8 rounded-lg flex items-center justify-center bg-indigo-100 text-indigo-600 hover:bg-indigo-200 transition-colors"
                    title="Voir détails"
                  >
                    <Eye class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- No Results -->
        <div v-if="filteredRequests.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
          <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
            <Search class="w-16 h-16 text-gray-400" />
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Aucune demande trouvée</h3>
          <p class="text-gray-500 mb-6 text-center">Essayez de modifier vos critères de recherche</p>
          <button 
            @click="resetFilters"
            class="flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition-colors shadow-md hover:shadow-lg"
          >
            <RotateCcw class="w-5 h-5" />
            <span>Réinitialiser les filtres</span>
          </button>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import { Tag, FileText, Calendar, Search, RotateCcw, Eye, Check, X } from 'lucide-vue-next';

export default {
  name: 'Demandes',
  components: { Tag, FileText, Calendar, Search, RotateCcw, Eye, Check, X },
  props: {
    requests: { type: Array, required: true }
  },
  data() {
    return {
      filters: {
        status: '',
        type: '',
        date: '',
        search: ''
      },
      filteredRequests: []
    };
  },
  methods: {
    applyFilters() {
      this.filteredRequests = this.requests.filter(req => {
        // Filtrage par Status
        const statusMatch = !this.filters.status || req.status === this.filters.status;
        
        // Filtrage par Type
        const typeMatch = !this.filters.type || req.typeDemande === this.filters.type;
        
        // Filtrage par Date (comparaison jour seulement)
        let dateMatch = true;
        if (this.filters.date) {
            const reqDate = new Date(req.dateDepot).toISOString().split('T')[0];
            dateMatch = reqDate === this.filters.date;
        }

        // Recherche textuelle (Reference ou Nom demandeur)
        let searchMatch = true;
        if (this.filters.search) {
            const searchTerm = this.filters.search.toLowerCase();
            const ref = (req.reference || '').toLowerCase();
            const nom = (req.demandeur && req.demandeur.nom) ? req.demandeur.nom.toLowerCase() : '';
            const prenom = (req.demandeur && req.demandeur.prenom) ? req.demandeur.prenom.toLowerCase() : '';
            
            searchMatch = ref.includes(searchTerm) || nom.includes(searchTerm) || prenom.includes(searchTerm);
        }

        return statusMatch && typeMatch && dateMatch && searchMatch;
      });
    },
    resetFilters() {
      this.filters = { status: '', type: '', date: '', search: '' };
      this.filteredRequests = [...this.requests];
    },
    viewRequest(req) {
      this.$router.push(`/admin/demande/${req.id}`);
    },
    formatDate(dateString) {
      if (!dateString) return '-';
      return new Date(dateString).toLocaleDateString('fr-FR', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      });
    },
    // Helpers pour les labels et styles

    getStatusLabel(status) {
      const labels = { 
        'SOUMISE': 'Soumise', 
        'EN_TRAITEMENT': 'En traitement',
        'VALIDEE': 'Validée', 
        'REJETEE': 'Rejetée',
        'TRAITEE': 'Traitée'
      };
      return labels[status] || status;
    },
    getStatusClass(status) {
      const classes = {
        'SOUMISE': 'bg-yellow-100 text-yellow-700',
        'EN_TRAITEMENT': 'bg-blue-100 text-blue-700',
        'VALIDEE': 'bg-green-100 text-green-700',
        'REJETEE': 'bg-red-100 text-red-700',
        'TRAITEE': 'bg-indigo-100 text-indigo-700'
      };
      return classes[status] || 'bg-gray-100 text-gray-700';
    },
    getStatusDotClass(status) {
       const classes = {
        'SOUMISE': 'bg-yellow-500 animate-pulse',
        'EN_TRAITEMENT': 'bg-blue-500',
        'VALIDEE': 'bg-green-500',
        'REJETEE': 'bg-red-500',
        'TRAITEE': 'bg-indigo-500'
      };
      return classes[status] || 'bg-gray-500';
    },
    async fetchDemandes() {
      // Placeholder for actual data fetching logic
      // For now, we'll just re-apply filters based on existing requests prop
      this.applyFilters();
    }
  },
  async mounted() {
    await this.fetchDemandes();
  },
  activated() {
    this.fetchDemandes();
  },
  watch: {
    requests: {
      handler() {
        this.applyFilters();
      },
      deep: true
    }
  }
};
</script>

<style scoped>
/* Style AdminHome - Filters + Table */
.demandes-admin {
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.filters-section {
  padding: 32px 32px 0 32px;
}

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.filter-icon {
  font-size: 16px;
}

.filter-input {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.filter-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-actions {
  display: flex;
  gap: 8px;
}

.btn-filter {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-filter.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-filter.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-filter.secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-filter.secondary:hover {
  background: #e5e7eb;
}

.table-section {
  padding: 0 32px 32px 32px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: white;
}

.table-count {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
  font-weight: 600;
}

.count-badge {
  background: white;
  color: #667eea;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 700;
}

.table-wrapper {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table thead {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.requests-table th {
  padding: 16px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.requests-table tbody tr {
  border-bottom: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.requests-table tbody tr:hover {
  background: #f9fafb;
  transform: scale(1.01);
}

.requests-table td {
  padding: 16px 20px;
  font-size: 14px;
  color: #374151;
}

.request-ref {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #667eea;
  background: #f0f4ff;
  padding: 4px 10px;
  border-radius: 6px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
}

.user-name {
  font-weight: 600;
  color: #1f2937;
}

.priority-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.priority-badge.high {
  background: #fee2e2;
  color: #dc2626;
}

.priority-badge.medium {
  background: #dbeafe;
  color: #2563eb;
}

.priority-badge.low {
  background: #f3f4f6;
  color: #6b7280;
}

.status-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  border: 2px solid;
}

.status-badge.pending {
  background: #fef3c7;
  color: #d97706;
  border-color: #fbbf24;
}

.status-badge.approved {
  background: #d1fae5;
  color: #059669;
  border-color: #34d399;
}

.status-badge.rejected {
  background: #fee2e2;
  color: #dc2626;
  border-color: #f87171;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-btn.approve {
  background: #d1fae5;
  color: #059669;
}

.action-btn.approve:hover:not(:disabled) {
  background: #059669;
  color: white;
  transform: scale(1.1);
}

.action-btn.reject {
  background: #fee2e2;
  color: #dc2626;
}

.action-btn.reject:hover:not(:disabled) {
  background: #dc2626;
  color: white;
  transform: scale(1.1);
}

.action-btn.view {
  background: #dbeafe;
  color: #2563eb;
}

.action-btn.view:hover {
  background: #2563eb;
  color: white;
  transform: scale(1.1);
}

.no-results {
  padding: 60px 20px;
  text-align: center;
  color: #9ca3af;
}

.no-results-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
}

.no-results p {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 20px;
}

.btn-reset-filter {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset-filter:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .filters-section,
  .table-section {
    padding: 20px;
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    flex-direction: column;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .requests-table {
    min-width: 800px;
  }
}
</style>