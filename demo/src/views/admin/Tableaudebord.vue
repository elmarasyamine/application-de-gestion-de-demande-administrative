<template>
  <div class="space-y-6">
    
    <!-- STATS SECTION -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div 
        v-for="(stat, index) in statsCards" 
        :key="index"
        class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <!-- Background decoration -->
        <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full -mr-12 -mt-12 opacity-50"></div>
        
        <div class="flex items-center justify-between mb-4 relative z-10">
          <div 
            :class="[
              'w-14 h-14 rounded-xl flex items-center justify-center shadow-md',
              stat.colorClass === 'blue' ? 'bg-gradient-to-br from-blue-400 to-blue-600 text-white' : '',
              stat.colorClass === 'green' ? 'bg-gradient-to-br from-green-400 to-green-600 text-white' : '',
              stat.colorClass === 'orange' ? 'bg-gradient-to-br from-orange-400 to-orange-600 text-white' : '',
              stat.colorClass === 'red' ? 'bg-gradient-to-br from-red-400 to-red-600 text-white' : '',
              stat.colorClass === 'purple' ? 'bg-gradient-to-br from-purple-400 to-purple-600 text-white' : ''
            ]"
            v-html="getIcon(stat.icon)"
          ></div>
          <span 
            :class="[
              'text-sm font-semibold px-3 py-1 rounded-full flex items-center gap-1',
              stat.trendClass === 'positive' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            ]"
          >
            <span v-html="getIcon(stat.trendClass === 'positive' ? 'TrendingUp' : 'TrendingDown', 14)"></span>
            {{ stat.trend }}
          </span>
        </div>
        
        <h3 class="text-3xl font-bold text-gray-800 mb-1 relative z-10">{{ stat.value }}</h3>
        <p class="text-gray-600 text-sm mb-3 relative z-10">{{ stat.label }}</p>
        
        <!-- Progress bar -->
        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden relative z-10">
          <div 
            :class="[
              'h-full rounded-full transition-all duration-500',
              stat.colorClass === 'blue' ? 'bg-gradient-to-r from-blue-400 to-blue-600' : '',
              stat.colorClass === 'green' ? 'bg-gradient-to-r from-green-400 to-green-600' : '',
              stat.colorClass === 'orange' ? 'bg-gradient-to-r from-orange-400 to-orange-600' : '',
              stat.colorClass === 'red' ? 'bg-gradient-to-r from-red-400 to-red-600' : '',
              stat.colorClass === 'purple' ? 'bg-gradient-to-r from-purple-400 to-purple-600' : ''
            ]"
            :style="{ width: stat.progress }"
          ></div>
        </div>
      </div>
    </section>

    <!-- CHARTS SECTION -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Chart 1: Bar Chart -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
        <h4 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span class="text-indigo-600" v-html="getIcon('BarChart3', 20)"></span>
          <span>Demandes par statut</span>
        </h4>
        <div class="flex items-end justify-around h-64 border-b border-gray-200 pb-2">
          <div 
            v-for="(item, index) in chartData" 
            :key="index"
            class="flex flex-col items-center gap-2 flex-1"
          >
            <div class="w-full flex flex-col items-center justify-end flex-1">
              <span class="text-sm font-semibold text-gray-700 mb-2">{{ item.value }}</span>
              <div 
                :class="[
                  'w-16 rounded-t-lg transition-all duration-500 hover:opacity-80 relative group',
                  item.className === 'pending' ? 'bg-gradient-to-t from-orange-400 to-orange-500' : '',
                  item.className === 'approved' ? 'bg-gradient-to-t from-green-400 to-green-500' : '',
                  item.className === 'rejected' ? 'bg-gradient-to-t from-red-400 to-red-500' : ''
                ]"
                :style="{ height: (item.value / maxChartValue * 100) + '%' }"
              ></div>
            </div>
            <span class="text-xs text-gray-600 font-medium text-center">{{ item.label }}</span>
          </div>
        </div>
      </div>

      <!-- Chart 2: Pie Chart -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
        <h4 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span class="text-indigo-600" v-html="getIcon('PieChart', 20)"></span>
          <span>Types de demandes</span>
        </h4>
        <div class="flex flex-col items-center">
          <svg viewBox="0 0 200 200" class="w-48 h-48 mb-4">
            <circle 
              v-for="(slice, index) in pieSlices"
              :key="index"
              :cx="100" 
              :cy="100" 
              :r="80"
              fill="none"
              :stroke="slice.color"
              :stroke-width="60"
              :stroke-dasharray="`${slice.percentage * 5.026} 502.6`"
              :stroke-dashoffset="slice.offset"
              transform="rotate(-90 100 100)"
              class="transition-all duration-300"
            />
          </svg>
          <div class="space-y-2 w-full">
            <div 
              v-for="(type, index) in typeData" 
              :key="index"
              class="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full" :style="{ backgroundColor: type.color }"></span>
                <span class="text-sm text-gray-700">{{ type.name }}</span>
              </div>
              <span class="text-sm font-semibold text-gray-800">{{ type.value }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart 3: Line Chart -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
        <h4 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span class="text-indigo-600" v-html="getIcon('LineChart', 20)"></span>
          <span>Activité hebdomadaire</span>
        </h4>
        <div class="space-y-4">
          <svg viewBox="0 0 300 160" class="w-full h-52">
            <defs>
              <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#8b5cf6;stop-opacity:0.4" />
                <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:0.05" />
              </linearGradient>
            </defs>
            <!-- Grille de fond -->
            <line v-for="i in 5" :key="'grid-'+i" x1="30" :x2="290" :y1="20 + i * 24" :y2="20 + i * 24" stroke="#e5e7eb" stroke-width="1" />
            <!-- Aire sous la courbe -->
            <polygon
              :points="lineChartAreaPoints"
              fill="url(#lineGradient)"
              class="transition-all duration-500"
            />
            <!-- Ligne principale -->
            <polyline
              :points="lineChartPoints"
              fill="none"
              stroke="#8b5cf6"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="transition-all duration-500"
            />
            <!-- Points avec valeurs -->
            <g v-for="(point, index) in weeklyData" :key="index">
              <circle
                :cx="35 + index * 40"
                :cy="140 - (point.demandes / maxWeeklyValue * 120)"
                r="6"
                fill="#8b5cf6"
                stroke="white"
                stroke-width="2"
                class="transition-all cursor-pointer hover:r-8"
              />
              <text
                v-if="point.demandes > 0"
                :x="35 + index * 40"
                :y="140 - (point.demandes / maxWeeklyValue * 120) - 12"
                text-anchor="middle"
                class="text-xs font-bold fill-indigo-700"
              >{{ point.demandes }}</text>
            </g>
          </svg>
          <div class="flex justify-around text-xs text-gray-600 font-medium mt-2">
            <span v-for="(day, idx) in weeklyData" :key="idx" class="text-center">
              <span class="block">{{ day.day }}</span>
            </span>
          </div>
        </div>
      </div>

    </section>

    <!-- REQUESTS TABLE -->
    <section class="bg-white rounded-2xl shadow-lg overflow-hidden">
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-indigo-50 to-purple-50">
        <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
          <span class="text-indigo-600" v-html="getIcon('ClipboardList', 22)"></span>
          <span>Dernières demandes</span>
        </h3>
        <button 
          @click="$router.push('/admin/demandes')"
          class="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition-colors"
        >
          <span v-html="getIcon('Eye', 18)"></span>
          <span>Voir tout</span>
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Référence</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Nom</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Type</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Date</th>

              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Statut</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="req in recentRequests" 
              :key="req.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4">
                <span class="font-mono text-sm font-semibold text-indigo-600">{{ req.reference }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-400 to-purple-600 flex items-center justify-center text-white font-bold shadow-md">
                    {{ (req.demandeur && req.demandeur.nom) ? req.demandeur.nom.charAt(0) : '?' }}
                  </div>
                  <span class="font-medium text-gray-800">{{ req.demandeur ? req.demandeur.nom + ' ' + req.demandeur.prenom : 'Inconnu' }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-700">{{ req.typeDemande }}</td>
              <td class="px-6 py-4 text-gray-600 text-sm">{{ formatDate(req.dateDepot) }}</td>

              <td class="px-6 py-4">
                <span 
                  :class="[
                    'inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold',
                    req.status === 'SOUMISE' || req.status === 'EN_TRAITEMENT' ? 'bg-yellow-100 text-yellow-700' : '',
                    req.status === 'VALIDEE' || req.status === 'TRAITEE' ? 'bg-green-100 text-green-700' : '',
                    req.status === 'REJETEE' ? 'bg-red-100 text-red-700' : ''
                  ]"
                >
                  <span v-html="getIcon(getStatusIcon(req.status), 12)"></span>
                  {{ getStatusLabel(req.status) }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">

                  <button 
                    @click="viewRequest(req)"
                    class="w-8 h-8 rounded-lg flex items-center justify-center bg-indigo-100 text-indigo-600 hover:bg-indigo-200 transition-colors"
                    title="Voir détails"
                    v-html="getIcon('Eye', 16)"
                  >
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="recentRequests.length === 0" class="flex flex-col items-center justify-center py-12">
          <span class="text-gray-300 mb-4" v-html="getIcon('Search', 64)"></span>
          <p class="text-gray-500 font-medium">Aucune demande trouvée</p>
        </div>
      </div>
    </section>

    <!-- ACTIVITIES SECTION -->
    <section class="bg-white rounded-2xl shadow-lg p-6">
      <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <span class="text-indigo-600" v-html="getIcon('Activity', 22)"></span>
        <span>Activités récentes</span>
      </h3>
      <div class="space-y-3">
        <div 
          v-for="(activity, index) in recentActivities" 
          :key="index"
          class="flex items-center gap-4 p-4 rounded-xl hover:bg-gray-50 transition-all duration-300 group"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform text-indigo-600">
            <span v-html="getIcon(activity.icon, 24)"></span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-gray-800 font-medium">{{ activity.text }}</p>
            <span class="text-sm text-gray-500">{{ activity.time }}</span>
          </div>
          <div 
            :class="[
              'w-3 h-3 rounded-full flex-shrink-0',
              activity.type === 'success' ? 'bg-green-400' : '',
              activity.type === 'warning' ? 'bg-orange-400' : '',
              activity.type === 'info' ? 'bg-blue-400' : ''
            ]"
          ></div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
export default {
  name: 'Tableaudebord',
  props: {
    requests: { type: Array, required: true },
    activities: { type: Array, required: true }
  },
  data() {
    return {
      // Couleurs pour les types de demandes
      typeColors: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444'],
      // SVG Icons library
      icons: {
        FileText: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
        Clock: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        CheckCircle2: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        XCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        TrendingUp: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" /></svg>',
        TrendingDown: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 014.306 6.43l.776 2.898m0 0l3.182-5.511m-3.182 5.511l-5.511-3.181" /></svg>',
        BarChart3: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>',
        PieChart: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z" /><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0013.5 3v7.5z" /></svg>',
        LineChart: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22" /></svg>',
        ClipboardList: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>',
        Eye: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>',
        Check: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>',
        X: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>',
        Search: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>',
        Activity: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13h4l3-9 4 18 3-9h4" /></svg>',
        AlertCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" /></svg>',
        AlertTriangle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>',
        CheckCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        UserCheck: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /><path stroke-linecap="round" stroke-linejoin="round" d="M16 11l2 2 4-4" /></svg>',
        UserX: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /><path stroke-linecap="round" stroke-linejoin="round" d="M17 11l4 4m0-4l-4 4" /></svg>',
        Bell: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>',
        Mail: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" /></svg>',
        Settings: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>',
        FileCheck: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        Calendar: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" /></svg>'
      }
    };
  },
  computed: {
    // ===== STATISTIQUES =====
    statsCards() {
      const total = this.totalRequests;
      const pending = this.pendingRequests;
      const approved = this.approvedRequests;
      const rejected = this.rejectedRequests;
      
      return [
        { 
          icon: 'FileText', 
          label: 'Total demandes', 
          value: total, 
          trend: total > 0 ? `${total}` : '0', 
          trendClass: 'positive',
          colorClass: 'blue',
          progress: '100%'
        },
        { 
          icon: 'Clock', 
          label: 'En attente', 
          value: pending, 
          trend: total > 0 ? `${Math.round(pending/total*100)}%` : '0%', 
          trendClass: pending > 0 ? 'positive' : 'negative',
          colorClass: 'orange',
          progress: total > 0 ? `${Math.round(pending/total*100)}%` : '0%'
        },
        { 
          icon: 'CheckCircle2', 
          label: 'Validées', 
          value: approved, 
          trend: total > 0 ? `${Math.round(approved/total*100)}%` : '0%', 
          trendClass: 'positive',
          colorClass: 'green',
          progress: total > 0 ? `${Math.round(approved/total*100)}%` : '0%'
        },
        { 
          icon: 'XCircle', 
          label: 'Rejetées', 
          value: rejected, 
          trend: total > 0 ? `${Math.round(rejected/total*100)}%` : '0%', 
          trendClass: 'negative',
          colorClass: 'red',
          progress: total > 0 ? `${Math.round(rejected/total*100)}%` : '0%'
        },
      ]
    },
    totalRequests() {
      return this.requests.length;
    },
    pendingRequests() {
      return this.requests.filter(r => r.status === 'SOUMISE' || r.status === 'EN_TRAITEMENT').length;
    },
    approvedRequests() {
      return this.requests.filter(r => r.status === 'VALIDEE' || r.status === 'TRAITEE').length;
    },
    rejectedRequests() {
      return this.requests.filter(r => r.status === 'REJETEE').length;
    },
    recentRequests() {
      return this.requests.slice(0, 6);
    },
    
    // ===== GRAPHIQUE PAR STATUT (BAR CHART) =====
    chartData() {
      return [
        { label: 'En attente', value: this.pendingRequests, className: 'pending' },
        { label: 'Validées', value: this.approvedRequests, className: 'approved' },
        { label: 'Rejetées', value: this.rejectedRequests, className: 'rejected' },
      ];
    },
    maxChartValue() {
      return Math.max(...this.chartData.map(item => item.value), 1);
    },
    
    // ===== TYPES DE DEMANDES (PIE CHART) - DONNÉES RÉELLES =====
    typeData() {
      if (this.requests.length === 0) {
        return [{ name: 'Aucune demande', value: 100, color: '#cbd5e1' }];
      }
      
      // Compter les demandes par type
      const typeCounts = {};
      this.requests.forEach(req => {
        const type = req.typeDemande || 'Non spécifié';
        typeCounts[type] = (typeCounts[type] || 0) + 1;
      });
      
      // Convertir en tableau avec pourcentages
      const total = this.requests.length;
      const types = Object.entries(typeCounts).map(([name, count], index) => ({
        name,
        value: Math.round((count / total) * 100),
        count,
        color: this.typeColors[index % this.typeColors.length]
      }));
      
      // Trier par count décroissant
      return types.sort((a, b) => b.count - a.count);
    },
    pieSlices() {
      let currentOffset = 0;
      const total = this.typeData.reduce((sum, t) => sum + t.value, 0);
      
      return this.typeData.map(type => {
        const percentage = type.value / total;
        const slice = {
          percentage,
          color: type.color,
          offset: -currentOffset * 5.026
        };
        currentOffset += percentage;
        return slice;
      });
    },
    
    // ===== ACTIVITÉ HEBDOMADAIRE (LINE CHART) - DONNÉES RÉELLES =====
    weeklyData() {
      const days = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
      const today = new Date();
      const weekData = [];
      
      // Générer les 7 derniers jours
      for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        const dayName = days[date.getDay()];
        const dateStr = date.toISOString().split('T')[0];
        
        // Compter les demandes pour ce jour
        const count = this.requests.filter(req => {
          const rawDate = req.dateDepot;
          if (!rawDate) return false;
          
          // Gérer le format de date backend (souvent timestamp ou ISO)
          const reqDateStr = new Date(rawDate).toISOString().split('T')[0];
          return reqDateStr === dateStr;
        }).length;
        
        weekData.push({
          day: dayName,
          demandes: count,
          date: dateStr
        });
      }
      
      return weekData;
    },
    maxWeeklyValue() {
      return Math.max(...this.weeklyData.map(d => d.demandes), 1);
    },
    lineChartPoints() {
      const maxVal = this.maxWeeklyValue;
      return this.weeklyData
        .map((point, index) => {
          const x = 35 + index * 40;
          const y = 140 - (point.demandes / maxVal * 120);
          return `${x},${y}`;
        })
        .join(' ');
    },
    lineChartAreaPoints() {
      const maxVal = this.maxWeeklyValue;
      const points = this.weeklyData.map((point, index) => {
        const x = 35 + index * 40;
        const y = 140 - (point.demandes / maxVal * 120);
        return `${x},${y}`;
      });
      // Fermer l'aire sous la courbe
      const firstX = 35;
      const lastX = 35 + (this.weeklyData.length - 1) * 40;
      return `${firstX},140 ${points.join(' ')} ${lastX},140`;
    },
    
    // ===== ACTIVITÉS RÉCENTES - DONNÉES RÉELLES =====
    recentActivities() {
      if (this.requests.length === 0) {
        return [{
          icon: 'FileText',
          text: 'Aucune activité récente',
          time: 'En attente de demandes',
          type: 'info'
        }];
      }
      
      // Créer des activités basées sur les demandes récentes
      return this.requests.slice(0, 5).map(req => {
        let icon, type;
        if (req.status === 'VALIDEE' || req.status === 'TRAITEE') {
          icon = 'CheckCircle2';
          type = 'success';
        } else if (req.status === 'REJETEE') {
          icon = 'XCircle';
          type = 'warning';
        } else {
          icon = 'Clock';
          type = 'info';
        }
        
        return {
          icon,
          text: `${req.reference || 'REQ'+req.id} - ${req.demandeur?.nom || 'Inconnu'} (${req.typeDemande})`,
          time: this.formatDate(req.dateDepot),
          type
        };
      });
    }
  },
  methods: {
    formatDate(dateString) {
        if (!dateString) return '-';
        try {
            return new Date(dateString).toLocaleDateString('fr-FR');
        } catch { return dateString; }
    },
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['FileText']
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`)
    },
    viewRequest(req) {
      this.$router.push(`/admin/demande/${req.id}`);
    },

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
    getStatusIcon(status) {
      const icons = {
        'SOUMISE': 'Clock',
        'EN_TRAITEMENT': 'Clock',
        'VALIDEE': 'CheckCircle2',
        'REJETEE': 'XCircle',
        'TRAITEE': 'CheckCircle2'
      }
      return icons[status] || 'Clock'
    },
    parseDate(dateStr) {
        // plus nécessaire avec Date() natif sur ISO string
      return dateStr;
    }
  }
};
</script>

<style scoped>
/* Animations */
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