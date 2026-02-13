<template>
  <div class="space-y-8">
    
    <!-- WELCOME BANNER -->
    <section class="relative overflow-hidden">
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 p-8">
        <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-indigo-100/30 to-violet-100/30 rounded-full blur-3xl -mr-48 -mt-24"></div>
        
        <div class="relative z-10 flex items-center justify-between">
          <div>
            <h1 class="text-4xl font-black bg-gradient-to-r from-slate-800 via-indigo-700 to-violet-700 bg-clip-text text-transparent mb-2">
              Bienvenue sur votre espace
            </h1>
            <p class="text-slate-600 font-semibold text-lg">Gérez vos demandes administratives en toute simplicité</p>
          </div>
          
          <button 
            @click="$emit('new-request')"
            class="group flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-bold shadow-xl shadow-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/40 transition-all duration-300 hover:scale-105 active:scale-95"
          >
            <span v-html="getIcon('PlusCircle', 24)" class="group-hover:rotate-90 transition-transform duration-300"></span>
            <span>Nouvelle demande</span>
          </button>
        </div>
      </div>
    </section>

    <!-- STATS SECTION -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div 
        v-for="(stat, index) in statsCards" 
        :key="index"
        class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative overflow-hidden group"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <!-- Background decoration -->
        <div :class="[
          'absolute top-0 right-0 w-32 h-32 rounded-full blur-2xl opacity-20 -mr-16 -mt-16 transition-all group-hover:scale-150',
          stat.colorClass === 'blue' ? 'bg-blue-400' : '',
          stat.colorClass === 'green' ? 'bg-green-400' : '',
          stat.colorClass === 'orange' ? 'bg-orange-400' : '',
          stat.colorClass === 'purple' ? 'bg-purple-400' : ''
        ]"></div>
        
        <div class="relative z-10">
          <!-- Header -->
          <div class="flex items-center justify-between mb-4">
            <div 
              :class="[
                'w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 text-white',
                stat.colorClass === 'blue' ? 'bg-gradient-to-br from-blue-400 to-blue-600' : '',
                stat.colorClass === 'green' ? 'bg-gradient-to-br from-green-400 to-green-600' : '',
                stat.colorClass === 'orange' ? 'bg-gradient-to-br from-orange-400 to-orange-600' : '',
                stat.colorClass === 'purple' ? 'bg-gradient-to-br from-purple-400 to-purple-600' : ''
              ]"
              v-html="getIcon(stat.icon, 28)"
            ></div>
            
            <div 
              :class="[
                'px-3 py-1.5 rounded-full text-sm font-bold flex items-center gap-1.5',
                stat.trendClass === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
              ]"
            >
              <span v-html="getIcon(stat.trendClass === 'up' ? 'TrendingUp' : 'TrendingDown', 16)"></span>
              <span>{{ stat.trend }}</span>
            </div>
          </div>
          
          <!-- Value -->
          <h3 class="text-4xl font-black text-slate-800 mb-1">{{ stat.value }}</h3>
          <p class="text-slate-600 font-semibold text-sm mb-4">{{ stat.label }}</p>
          
          <!-- Progress bar -->
          <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div 
              :class="[
                'h-full rounded-full transition-all duration-1000 ease-out',
                stat.colorClass === 'blue' ? 'bg-gradient-to-r from-blue-400 to-blue-600' : '',
                stat.colorClass === 'green' ? 'bg-gradient-to-r from-green-400 to-green-600' : '',
                stat.colorClass === 'orange' ? 'bg-gradient-to-r from-orange-400 to-orange-600' : '',
                stat.colorClass === 'purple' ? 'bg-gradient-to-r from-purple-400 to-purple-600' : ''
              ]"
              :style="{ width: stat.progress }"
            ></div>
          </div>
        </div>
      </div>
    </section>

    <!-- REQUESTS TABLE -->
    <section class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 overflow-hidden">
      
      <!-- Table Header -->
      <div class="relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-600"></div>
        <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAgTSAwIDIwIEwgNDAgMjAgTSAyMCAwIEwgMjAgNDAgTSAwIDMwIEwgNDAgMzAgTSAzMCAwIEwgMzAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-40"></div>
        
        <div class="relative z-10 px-8 py-6 flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-bold text-white mb-1 flex items-center gap-3">
              <span v-html="getIcon('ClipboardList', 32)" class="text-white"></span>
              <span>Mes dernières demandes</span>
            </h3>
            <p class="text-indigo-100 font-medium">Suivez l'évolution de vos demandes en temps réel</p>
          </div>
          
          <button 
            @click="$emit('view-all-requests')"
            class="group flex items-center gap-3 px-6 py-3 rounded-2xl bg-white/20 backdrop-blur-sm border border-white/30 text-white font-bold hover:bg-white/30 transition-all hover:scale-105"
          >
            <span v-html="getIcon('Eye', 20)"></span>
            <span>Voir tout</span>
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-slate-50/80 backdrop-blur-sm border-b-2 border-slate-200">
            <tr>
              <th class="px-6 py-4 text-left">
                <div class="flex items-center gap-2 text-xs font-black text-slate-600 uppercase tracking-widest">
                  <span>Référence</span>
                  <span v-html="getIcon('ArrowUpDown', 16)" class="text-slate-400"></span>
                </div>
              </th>
              <th class="px-6 py-4 text-left">
                <div class="text-xs font-black text-slate-600 uppercase tracking-widest">Type</div>
              </th>
              <th class="px-6 py-4 text-left">
                <div class="text-xs font-black text-slate-600 uppercase tracking-widest">Date de dépôt</div>
              </th>
              <th class="px-6 py-4 text-left">
                <div class="text-xs font-black text-slate-600 uppercase tracking-widest">Statut</div>
              </th>
              <th class="px-6 py-4 text-center">
                <div class="text-xs font-black text-slate-600 uppercase tracking-widest">Action</div>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr 
              v-for="(req, index) in recentRequests" 
              :key="req.id"
              class="group hover:bg-gradient-to-r hover:from-indigo-50/50 hover:to-violet-50/50 transition-all duration-300"
              :style="{ animationDelay: `${index * 0.05}s` }"
            >
              <!-- Référence -->
              <td class="px-6 py-5">
                <div class="flex items-center gap-3">
                  <div class="w-1 h-14 rounded-full bg-gradient-to-b from-indigo-500 to-violet-600 group-hover:h-16 transition-all duration-300"></div>
                  <div class="font-mono text-sm font-bold text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-xl group-hover:bg-indigo-100 transition-colors">
                    {{ req.ref }}
                  </div>
                </div>
              </td>
              
              <!-- Type -->
              <td class="px-6 py-5">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span v-html="getIcon(getTypeIcon(req.typeLabel), 20)" class="text-slate-600"></span>
                  </div>
                  <span class="font-bold text-slate-700">{{ req.typeLabel }}</span>
                </div>
              </td>
              
              <!-- Date -->
              <td class="px-6 py-5">
                <div class="flex items-center gap-2 text-slate-600">
                  <span v-html="getIcon('Calendar', 20)" class="text-slate-400"></span>
                  <span class="font-semibold">{{ formatDate(req.date) }}</span>
                </div>
              </td>
              
              <!-- Statut -->
              <td class="px-6 py-5">
                <div 
                  :class="[
                    'inline-flex items-center gap-2.5 px-4 py-2.5 rounded-xl font-bold text-sm shadow-sm',
                    req.status === 'pending' ? 'bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 text-amber-700' : '',
                    req.status === 'approved' ? 'bg-gradient-to-r from-emerald-50 to-green-50 border-2 border-emerald-200 text-emerald-700' : '',
                    req.status === 'rejected' ? 'bg-gradient-to-r from-rose-50 to-red-50 border-2 border-rose-200 text-rose-700' : '',
                    req.status === 'processing' ? 'bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 text-blue-700' : ''
                  ]"
                >
                  <span 
                    :class="[
                      'w-2.5 h-2.5 rounded-full',
                      req.status === 'pending' ? 'bg-amber-500 animate-pulse' : '',
                      req.status === 'approved' ? 'bg-emerald-500' : '',
                      req.status === 'rejected' ? 'bg-rose-500' : '',
                      req.status === 'processing' ? 'bg-blue-500 animate-pulse' : ''
                    ]"
                  ></span>
                  <span>{{ req.statusLabel }}</span>
                </div>
              </td>
              
              <!-- Action -->
              <td class="px-6 py-5">
                <div class="flex items-center justify-center">
                  <button 
                    @click="$emit('view-request', req.id)"
                    class="group/btn w-11 h-11 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white flex items-center justify-center shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/50 transition-all duration-300 hover:scale-110 active:scale-95"
                    title="Voir détails"
                  >
                    <span v-html="getIcon('Eye', 24)"></span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="recentRequests.length === 0" class="flex flex-col items-center justify-center py-20 px-4">
          <div class="relative mb-8">
            <div class="w-32 h-32 rounded-3xl bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-br from-indigo-100/30 to-violet-100/30"></div>
              <span v-html="getIcon('ClipboardList', 64)" class="text-slate-400 relative z-10"></span>
            </div>
            <div class="absolute -top-2 -right-2 w-8 h-8 bg-indigo-400 rounded-full animate-bounce"></div>
          </div>
          
          <h3 class="text-3xl font-bold text-slate-800 mb-3">Aucune demande pour le moment</h3>
          <p class="text-slate-600 font-medium mb-8 text-center max-w-md">
            Vous n'avez pas encore soumis de demande. Commencez dès maintenant !
          </p>
          
          <button 
            @click="$emit('new-request')"
            class="group flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-bold shadow-xl shadow-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/40 transition-all duration-300 hover:scale-105 active:scale-95"
          >
            <span v-html="getIcon('PlusCircle', 24)" class="group-hover:rotate-90 transition-transform duration-300"></span>
            <span>Créer une nouvelle demande</span>
          </button>
        </div>
      </div>
    </section>

    <!-- QUICK ACTIONS -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Guide -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center mb-4 shadow-lg text-white">
          <span v-html="getIcon('BookOpen', 28)"></span>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-2">Guide d'utilisation</h3>
        <p class="text-slate-600 font-medium mb-4">Découvrez comment utiliser la plateforme efficacement</p>
        <button class="flex items-center gap-2 text-blue-600 font-bold hover:gap-3 transition-all">
          <span>En savoir plus</span>
          <span v-html="getIcon('ChevronRight', 20)"></span>
        </button>
      </div>

      <!-- Support -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-green-600 flex items-center justify-center mb-4 shadow-lg text-white">
          <span v-html="getIcon('MessageCircle', 28)"></span>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-2">Support technique</h3>
        <p class="text-slate-600 font-medium mb-4">Besoin d'aide ? Notre équipe est là pour vous</p>
        <button class="flex items-center gap-2 text-emerald-600 font-bold hover:gap-3 transition-all">
          <span>Contacter le support</span>
          <span v-html="getIcon('ChevronRight', 20)"></span>
        </button>
      </div>

      <!-- FAQ -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-violet-400 to-purple-600 flex items-center justify-center mb-4 shadow-lg text-white">
          <span v-html="getIcon('HelpCircle', 28)"></span>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-2">Questions fréquentes</h3>
        <p class="text-slate-600 font-medium mb-4">Trouvez rapidement des réponses à vos questions</p>
        <button class="flex items-center gap-2 text-violet-600 font-bold hover:gap-3 transition-all">
          <span>Consulter la FAQ</span>
          <span v-html="getIcon('ChevronRight', 20)"></span>
        </button>
      </div>
    </section>

  </div>
</template>

<script>
import { getMesDemandes } from '@/services/demandeService';

export default {
  data() {
    return {
      demandes: [], // Real data from backend
      loading: true,
      error: null,
      // SVG Icons library
      icons: {
        PlusCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        BarChart3: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>',
        CheckCircle2: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        Clock: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        TrendingUp: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" /></svg>',
        TrendingDown: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 014.306 6.43l.776 2.898m0 0l3.182-5.511m-3.182 5.511l-5.511-3.181" /></svg>',
        ClipboardList: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>',
        Eye: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>',
        ArrowUpDown: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" /></svg>',
        Calendar: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>',
        Home: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>',
        GraduationCap: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" /></svg>',
        Baby: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" /></svg>',
        FileText: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
        File: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" /></svg>',
        BookOpen: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>',
        MessageCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" /></svg>',
        HelpCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" /></svg>',
        ChevronRight: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" /></svg>'
      }
    }
  },
  computed: {
    // Compute stats from real data
    statsCards() {
      const total = this.demandes.length;
      const validees = this.demandes.filter(d => d.status === 'VALIDEE').length;
      const enAttente = this.demandes.filter(d => d.status === 'SOUMISE').length;
      const enTraitement = this.demandes.filter(d => d.status === 'EN_TRAITEMENT').length;
      
      return [
        { 
          icon: 'BarChart3', 
          value: total.toString(), 
          label: 'Demandes totales', 
          trend: '+' + total, 
          trendClass: 'up', 
          colorClass: 'blue', 
          progress: '100%' 
        },
        { 
          icon: 'CheckCircle2', 
          value: validees.toString(), 
          label: 'Approuvées', 
          trend: '+' + validees, 
          trendClass: 'up', 
          colorClass: 'green', 
          progress: total > 0 ? Math.round((validees / total) * 100) + '%' : '0%'
        },
        { 
          icon: 'Clock', 
          value: enAttente.toString(), 
          label: 'En attente', 
          trend: '+' + enAttente, 
          trendClass: 'up', 
          colorClass: 'orange', 
          progress: total > 0 ? Math.round((enAttente / total) * 100) + '%' : '0%'
        },
        { 
          icon: 'TrendingUp', 
          value: enTraitement.toString(), 
          label: 'En traitement', 
          trend: '+' + enTraitement, 
          trendClass: 'up', 
          colorClass: 'purple', 
          progress: total > 0 ? Math.round((enTraitement / total) * 100) + '%' : '0%'
        }
      ];
    },
    // Map backend data to UI format
    recentRequests() {
      const statusMap = {
        'SOUMISE': { status: 'pending', label: 'En attente' },
        'EN_TRAITEMENT': { status: 'processing', label: 'En traitement' },
        'VALIDEE': { status: 'approved', label: 'Approuvée' },
        'REJETEE': { status: 'rejected', label: 'Rejetée' }
      };
      
      return this.demandes.slice(0, 5).map(d => ({
        id: d.id,
        ref: d.reference || 'REF-' + d.id,
        typeLabel: d.typeDemande || d.titreDemande,
        date: d.dateDepot,
        status: statusMap[d.status]?.status || 'pending',
        statusLabel: statusMap[d.status]?.label || 'En attente'
      }));
    }
  },
  async mounted() {
    await this.fetchDemandes();
  },
  methods: {
    async fetchDemandes() {
      this.loading = true;
      this.error = null;
      try {
        // Get user from localStorage (saved during login)
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          this.error = 'Utilisateur non connecté';
          this.loading = false;
          return;
        }
        const user = JSON.parse(userStr);
        const response = await getMesDemandes(user.id);
        this.demandes = response.data;
      } catch (err) {
        console.error('Erreur lors du chargement des demandes:', err);
        this.error = 'Impossible de charger vos demandes';
      } finally {
        this.loading = false;
      }
    },
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['FileText']
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`)
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      const date = new Date(dateStr)
      return date.toLocaleDateString('fr-FR', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
      })
    },
    getTypeIcon(type) {
      const icons = {
        'Certificat de résidence': 'Home',
        'Attestation de scolarité': 'GraduationCap',
        'Extrait de naissance': 'Baby',
        'Certificat': 'FileText',
        'Attestation': 'ClipboardList',
        'Justificatif': 'File'
      }
      return icons[type] || 'FileText'
    }
  }
}
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

.space-y-8 > section {
  animation: fadeInUp 0.5s ease-out forwards;
}
</style>