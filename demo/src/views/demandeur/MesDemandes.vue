<template>
  <div class="space-y-6">
    
    <!-- FILTERS SECTION -->
    <section class="bg-white rounded-2xl shadow-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- Statut Filter -->
        <div class="group">
          <label class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-2">
            <span v-html="getIcon('Tag', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
            <span>Statut</span>
          </label>
          <div class="relative">
            <select 
              v-model="filters.status" 
              class="w-full px-4 py-2.5 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all bg-white font-medium shadow-sm hover:border-indigo-400 appearance-none cursor-pointer"
            >
              <option value="">Tous les statuts</option>
              <option value="en_attente">En attente</option>
              <option value="en_cours">En cours</option>
              <option value="validee">Validée</option>
              <option value="rejetee">Rejetée</option>
            </select>
            <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-indigo-600">
              <span v-html="getIcon('ChevronDown', 20)"></span>
            </div>
          </div>
        </div>

        <!-- Type Filter -->
        <div class="group">
          <label class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-2">
            <span v-html="getIcon('FileText', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
            <span>Type</span>
          </label>
          <div class="relative">
            <select 
              v-model="filters.type" 
              class="w-full px-4 py-2.5 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all bg-white font-medium shadow-sm hover:border-indigo-400 appearance-none cursor-pointer"
            >
              <option value="">Tous les types</option>
              <option value="Attestation de scolarité">Attestation de scolarité</option>
              <option value="Relevé de notes">Relevé de notes</option>
              <option value="Certificat de réussite">Certificat de réussite</option>
              <option value="Convention de stage">Convention de stage</option>
              <option value="Autre">Autre</option>
            </select>
            <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-indigo-600">
              <span v-html="getIcon('ChevronDown', 20)"></span>
            </div>
          </div>
        </div>

        <!-- Date Filter -->
        <div class="group">
          <label class="flex items-center gap-2 text-sm font-bold text-gray-700 mb-2">
            <span v-html="getIcon('Calendar', 20)" class="text-indigo-600 group-hover:scale-110 transition-transform"></span>
            <span>Date</span>
          </label>
          <input 
            type="date" 
            v-model="filters.date" 
            class="w-full px-4 py-2.5 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium shadow-sm hover:border-indigo-400 cursor-pointer"
          >
        </div>

        <!-- Action Buttons -->
        <div class="flex items-end gap-2">
          <button 
            @click="applyFilters"
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            <span v-html="getIcon('Search', 20)"></span>
            <span class="hidden sm:inline">Filtrer</span>
          </button>
          <button 
            @click="resetFilters"
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border-2 border-gray-300 text-gray-700 font-bold hover:bg-gray-50 hover:border-gray-400 transition-all shadow-md hover:shadow-lg"
          >
            <span v-html="getIcon('RotateCcw', 20)"></span>
            <span class="hidden sm:inline">Reset</span>
          </button>
        </div>
      </div>
    </section>

    <!-- TABLE SECTION -->
    <section class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
      
      <!-- Table Header -->
      <div class="flex items-center justify-between px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50">
        <h3 class="text-2xl font-bold text-gray-800 flex items-center gap-3">
          <span v-html="getIcon('ClipboardList', 28)" class="text-indigo-600"></span>
          <span>Toutes mes demandes</span>
        </h3>
        <div class="flex items-center gap-2 bg-white/60 backdrop-blur-sm px-5 py-2.5 rounded-full shadow-md">
          <span class="text-xl font-bold text-indigo-600">{{ filteredRequests.length }}</span>
          <span class="text-sm text-gray-600 font-semibold">demande(s)</span>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gradient-to-r from-gray-50 to-gray-100 border-b-2 border-gray-200">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                Référence
              </th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                Date de dépôt
              </th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                Statut
              </th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                Action
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="req in filteredRequests" 
              :key="req.id"
              class="hover:bg-gradient-to-r hover:from-indigo-50/50 hover:to-purple-50/50 transition-all"
            >
              <!-- Référence -->
              <td class="px-6 py-4">
                <span class="font-mono text-sm font-bold text-indigo-600 bg-indigo-50 px-4 py-2 rounded-lg shadow-sm">
                  {{ req.ref }}
                </span>
              </td>
              
              <!-- Type -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <span v-html="getIcon(getTypeIconName(req.type), 20)" class="text-gray-600"></span>
                  <span class="font-semibold text-gray-800">{{ req.typeLabel }}</span>
                </div>
              </td>
              
              <!-- Date -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <span v-html="getIcon('Calendar', 18)" class="text-gray-500"></span>
                  <span class="text-gray-700 font-medium">{{ formatDate(req.date) }}</span>
                </div>
              </td>
              
              <!-- Statut -->
              <td class="px-6 py-4">
                <span 
                  :class="[
                    'inline-flex items-center px-4 py-2 rounded-full text-xs font-bold shadow-sm',
                    req.status === 'en_attente' ? 'bg-yellow-100 text-yellow-700 border-2 border-yellow-300' : '',
                    req.status === 'en_cours' ? 'bg-blue-100 text-blue-700 border-2 border-blue-300' : '',
                    req.status === 'validee' ? 'bg-green-100 text-green-700 border-2 border-green-300' : '',
                    req.status === 'rejetee' ? 'bg-red-100 text-red-700 border-2 border-red-300' : '',
                    req.status === 'annulee' ? 'bg-gray-100 text-gray-700 border-2 border-gray-300' : ''
                  ]"
                >
                  <span 
                    :class="[
                      'w-2 h-2 rounded-full mr-2',
                      req.status === 'en_attente' ? 'bg-yellow-500 animate-pulse' : '',
                      req.status === 'en_cours' ? 'bg-blue-500 animate-pulse' : '',
                      req.status === 'validee' ? 'bg-green-500' : '',
                      req.status === 'rejetee' ? 'bg-red-500' : '',
                      req.status === 'annulee' ? 'bg-gray-500' : ''
                    ]"
                  ></span>
                  {{ req.statusLabel }}
                </span>
              </td>
              
              <!-- Actions -->
              <td class="px-6 py-4">
                <button 
                  @click="viewRequest(req.id)"
                  class="w-10 h-10 rounded-xl flex items-center justify-center bg-indigo-100 text-indigo-600 hover:bg-indigo-200 hover:scale-110 transition-all shadow-md hover:shadow-lg"
                  title="Voir détails"
                >
                  <span v-html="getIcon('Eye', 20)"></span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- No Results -->
        <div v-if="filteredRequests.length === 0" class="flex flex-col items-center justify-center py-20 px-4">
          <div class="w-28 h-28 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mb-6 shadow-lg">
            <span v-html="getIcon('Search', 56)" class="text-gray-400"></span>
          </div>
          <h3 class="text-2xl font-bold text-gray-800 mb-2">Aucune demande trouvée</h3>
          <p class="text-gray-500 mb-6 text-center text-lg">Essayez de modifier vos critères de recherche</p>
          <button 
            @click="resetFilters"
            class="flex items-center gap-3 px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
          >
            <span v-html="getIcon('RotateCcw', 20)"></span>
            <span>Réinitialiser les filtres</span>
          </button>
        </div>
      </div>
    </section>

    <!-- MODAL DETAIL DEMANDE -->
    <div v-if="selectedRequest" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto transform transition-all">
        
        <!-- Modal Header -->
        <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-5 rounded-t-2xl">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-bold text-white flex items-center gap-3">
              <span v-html="getIcon('FileText', 24)"></span>
              Détails de la demande
            </h3>
            <button @click="closeModal" class="w-8 h-8 bg-white/20 hover:bg-white/30 rounded-lg flex items-center justify-center text-white transition-all">
              <span v-html="getIcon('X', 20)"></span>
            </button>
          </div>
        </div>
        
        <!-- Modal Body -->
        <div class="p-6 space-y-4">
          
          <!-- Référence -->
          <div class="flex items-start gap-4 p-4 rounded-xl bg-indigo-50 border-2 border-indigo-200">
            <div class="w-12 h-12 bg-indigo-500 rounded-xl flex items-center justify-center text-white shadow-md">
              <span v-html="getIcon('Tag', 24)"></span>
            </div>
            <div>
              <div class="text-sm font-bold text-gray-600">Référence</div>
              <div class="text-lg font-bold text-indigo-600">{{ selectedRequest.ref }}</div>
            </div>
          </div>
          
          <!-- Type -->
          <div class="flex items-start gap-4 p-4 rounded-xl bg-blue-50 border-2 border-blue-200">
            <div class="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center text-white shadow-md">
              <span v-html="getIcon('ClipboardList', 24)"></span>
            </div>
            <div>
              <div class="text-sm font-bold text-gray-600">Type de demande</div>
              <div class="text-lg font-bold text-gray-800">{{ selectedRequest.typeLabel }}</div>
            </div>
          </div>
          
          <!-- Titre -->
          <div v-if="selectedRequest.titre" class="flex items-start gap-4 p-4 rounded-xl bg-purple-50 border-2 border-purple-200">
            <div class="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center text-white shadow-md">
              <span v-html="getIcon('FileText', 24)"></span>
            </div>
            <div>
              <div class="text-sm font-bold text-gray-600">Titre</div>
              <div class="text-lg font-bold text-gray-800">{{ selectedRequest.titre }}</div>
            </div>
          </div>
          
          <!-- Description -->
          <div v-if="selectedRequest.description" class="flex items-start gap-4 p-4 rounded-xl bg-gray-50 border-2 border-gray-200">
            <div class="w-12 h-12 bg-gray-500 rounded-xl flex items-center justify-center text-white shadow-md">
              <span v-html="getIcon('FileText', 24)"></span>
            </div>
            <div class="flex-1">
              <div class="text-sm font-bold text-gray-600">Description</div>
              <div class="text-gray-700 mt-1">{{ selectedRequest.description }}</div>
            </div>
          </div>
          
          <!-- Statut -->
          <div class="flex items-start gap-4 p-4 rounded-xl border-2" :class="getStatusBgClass(selectedRequest.status)">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shadow-md" :class="getStatusIconBgClass(selectedRequest.status)">
              <span v-html="getIcon('CheckCircle', 24)"></span>
            </div>
            <div>
              <div class="text-sm font-bold text-gray-600">Statut</div>
              <div class="text-lg font-bold" :class="getStatusTextClass(selectedRequest.status)">{{ selectedRequest.statusLabel }}</div>
            </div>
          </div>
          
          <!-- Date -->
          <div class="flex items-start gap-4 p-4 rounded-xl bg-green-50 border-2 border-green-200">
            <div class="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center text-white shadow-md">
              <span v-html="getIcon('Calendar', 24)"></span>
            </div>
            <div>
              <div class="text-sm font-bold text-gray-600">Date de dépôt</div>
              <div class="text-lg font-bold text-gray-800">{{ formatDate(selectedRequest.date) }}</div>
            </div>
          </div>
          
        </div>
        
        <!-- Modal Footer -->
        <div class="px-6 py-4 border-t border-gray-200 flex justify-end">
          <button @click="closeModal" class="px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg">
            Fermer
          </button>
        </div>
        
      </div>
    </div>

  </div>
</template>

<script>
import { getMesDemandes } from '@/services/demandeService';

export default {
  name: 'MesDemandesVue',
  data() {
    return {
      filters: {
        status: '',
        type: '',
        date: ''
      },
      allRequests: [],
      filteredRequests: [],
      selectedRequest: null,
      loading: true,
      error: null,
      // Status mapping from backend to frontend
      statusMap: {
        'SOUMISE': { status: 'en_attente', label: 'En attente' },
        'EN_TRAITEMENT': { status: 'en_cours', label: 'En cours' },
        'VALIDEE': { status: 'validee', label: 'Validée' },
        'REJETEE': { status: 'rejetee', label: 'Rejetée' }
      },
      // Bibliothèque d'icônes SVG
      icons: {
        Tag: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" /><path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z" /></svg>',
        FileText: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
        Calendar: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>',
        ChevronDown: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" /></svg>',
        Search: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>',
        RotateCcw: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" /></svg>',
        ClipboardList: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>',
        Eye: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>',
        FileCheck: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        BarChart: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>',
        Award: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 002.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 012.916.52 6.003 6.003 0 01-5.395 4.972m0 0a6.726 6.726 0 01-2.749 1.35m0 0a6.772 6.772 0 01-3.044 0" /></svg>',
        Briefcase: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z" /></svg>',
        File: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>',
        X: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>',
        CheckCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
      }
    };
  },
  methods: {
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['FileText'];
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`);
    },
    
    getTypeIconName(type) {
      const iconMap = {
        'Attestation de scolarité': 'FileCheck',
        'Relevé de notes': 'BarChart',
        'Certificat de réussite': 'Award',
        'Convention de stage': 'Briefcase',
        'Autre': 'File'
      };
      return iconMap[type] || 'FileText';
    },
    
    async fetchDemandes() {
      this.loading = true;
      this.error = null;
      try {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          this.error = 'Utilisateur non connecté';
          this.loading = false;
          return;
        }
        const user = JSON.parse(userStr);
        const response = await getMesDemandes(user.id);
        
        // Map backend data to frontend format
        this.allRequests = response.data.map(d => ({
          id: d.id,
          ref: d.reference || 'REF-' + d.id,
          type: d.typeDemande,
          typeLabel: d.typeDemande || d.titreDemande,
          titre: d.titreDemande,
          description: d.description,
          date: d.dateDepot,
          status: this.statusMap[d.status]?.status || 'en_attente',
          statusLabel: this.statusMap[d.status]?.label || 'En attente'
        }));
        
        this.filteredRequests = [...this.allRequests];
      } catch (err) {
        console.error('Erreur lors du chargement des demandes:', err);
        this.error = 'Impossible de charger vos demandes';
      } finally {
        this.loading = false;
      }
    },
    
    applyFilters() {
      this.filteredRequests = this.allRequests.filter(req => {
        const statusMatch = !this.filters.status || req.status === this.filters.status;
        const typeMatch = !this.filters.type || req.type === this.filters.type;
        const dateMatch = !this.filters.date || (req.date && req.date.startsWith(this.filters.date));
        return statusMatch && typeMatch && dateMatch;
      });
    },
    
    resetFilters() {
      this.filters = {
        status: '',
        type: '',
        date: ''
      };
      this.filteredRequests = [...this.allRequests];
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    viewRequest(id) {
      const request = this.allRequests.find(r => r.id === id);
      if (request) {
        this.selectedRequest = request;
      }
    },
    
    closeModal() {
      this.selectedRequest = null;
    },
    
    getStatusBgClass(status) {
      const map = {
        'en_attente': 'bg-yellow-50 border-yellow-200',
        'en_cours': 'bg-blue-50 border-blue-200',
        'validee': 'bg-green-50 border-green-200',
        'rejetee': 'bg-red-50 border-red-200'
      };
      return map[status] || 'bg-gray-50 border-gray-200';
    },
    
    getStatusIconBgClass(status) {
      const map = {
        'en_attente': 'bg-yellow-500',
        'en_cours': 'bg-blue-500',
        'validee': 'bg-green-500',
        'rejetee': 'bg-red-500'
      };
      return map[status] || 'bg-gray-500';
    },
    
    getStatusTextClass(status) {
      const map = {
        'en_attente': 'text-yellow-700',
        'en_cours': 'text-blue-700',
        'validee': 'text-green-700',
        'rejetee': 'text-red-700'
      };
      return map[status] || 'text-gray-700';
    }
  },
  
  async mounted() {
    await this.fetchDemandes();
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