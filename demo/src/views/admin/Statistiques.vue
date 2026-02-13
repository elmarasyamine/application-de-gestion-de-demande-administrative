<template>
  <div class="space-y-8 pb-12">
    
    <!-- EXPORT SECTION - Premium Design -->
    <section class="relative overflow-hidden">
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 p-8">
        
        <!-- Decorative background -->
        <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-emerald-100/30 to-teal-100/30 rounded-full blur-3xl -mr-48 -mt-48"></div>
        <div class="absolute bottom-0 left-0 w-72 h-72 bg-gradient-to-tr from-blue-100/30 to-cyan-100/30 rounded-full blur-3xl -ml-36 -mb-36"></div>
        
        <div class="relative z-10">
          <div class="flex flex-col md:flex-row items-start justify-between mb-8 gap-4">
            <div>
              <h3 class="text-2xl font-bold text-slate-800 mb-2 flex items-center gap-3">
                <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg">
                  <BarChart3 class="w-6 h-6" />
                </div>
                <span>Exporter le rapport complet</span>
              </h3>
              <p class="text-slate-600 font-medium ml-1 flex items-center gap-2">
                 <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                 Générez vos rapports de statistiques basés sur {{ requests.length }} demandes
              </p>
            </div>
            
            <!-- Period Selector -->
            <div class="relative group">
              <select 
                v-model="exportPeriod" 
                class="pl-5 pr-12 py-3.5 rounded-2xl border-2 border-slate-200 focus:border-indigo-500 focus:outline-none transition-all bg-white font-bold text-slate-700 appearance-none cursor-pointer shadow-sm hover:shadow-md"
              >
                <option value="all">Période globale</option>
                <option value="month">Mois en cours</option>
                <option value="year">Année en cours</option>
              </select>
              <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                <ChevronDown class="w-5 h-5" />
              </div>
            </div>
          </div>

          <!-- Export Buttons Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Excel Export -->
            <button 
              @click="exportExcel"
              class="group relative overflow-hidden bg-white hover:bg-emerald-50 border-2 border-slate-100 hover:border-emerald-200 rounded-3xl p-6 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 active:scale-95"
            >
              <div class="flex items-center gap-5">
                <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-white shadow-lg shadow-emerald-500/20 group-hover:scale-110 transition-transform">
                  <TableProperties class="w-8 h-8" />
                </div>
                <div class="flex-1 text-left">
                  <h4 class="text-xl font-bold text-slate-800 mb-1 group-hover:text-emerald-700 transition-colors">Excel</h4>
                  <p class="text-sm text-slate-500 font-medium">Analyse de données</p>
                </div>
              </div>
            </button>

            <!-- CSV Export -->
            <button 
              @click="exportCSV"
              class="group relative overflow-hidden bg-white hover:bg-blue-50 border-2 border-slate-100 hover:border-blue-200 rounded-3xl p-6 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 active:scale-95"
            >
              <div class="flex items-center gap-5">
                <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform">
                  <Download class="w-8 h-8" />
                </div>
                <div class="flex-1 text-left">
                  <h4 class="text-xl font-bold text-slate-800 mb-1 group-hover:text-blue-700 transition-colors">CSV</h4>
                  <p class="text-sm text-slate-500 font-medium">Import simple</p>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- CHARTS SECTION -->
    <section class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      <!-- Évolution mensuelle -->
      <div class="lg:col-span-8 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 overflow-hidden">
        <div class="p-8 border-b border-slate-100 flex items-center justify-between">
            <h4 class="text-xl font-bold text-slate-800 flex items-center gap-3">
              <TrendingUp class="w-6 h-6 text-indigo-600" />
              <span>Volume des demandes ({{currentYear}})</span>
            </h4>
        </div>

        <div class="p-8">
          <div class="relative h-64 w-full">
            <svg viewBox="0 0 600 240" class="w-full h-full">
              <defs>
                <linearGradient id="chartLineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#6366f1;stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:#6366f1;stop-opacity:0" />
                </linearGradient>
              </defs>

              <line v-for="i in 5" :key="i" x1="40" :y1="i*40" x2="560" :y2="i*40" stroke="#f1f5f9" stroke-width="2" />
              <path :d="chartAreaPath" fill="url(#chartLineGradient)" />
              <path :d="chartLinePath" fill="none" stroke="#6366f1" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
              <circle v-for="(point, idx) in monthlyChartPoints" :key="idx" :cx="point.x" :cy="point.y" r="6" fill="white" stroke="#6366f1" stroke-width="3" class="cursor-pointer hover:r-8 transition-all duration-300" />
            </svg>
            <div class="flex justify-between px-10 mt-4">
              <span v-for="m in monthLabelsShort" :key="m" class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">{{ m }}</span>
            </div>
          </div>

          <!-- Bottom Summary -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
            <div class="p-5 rounded-3xl bg-slate-50 border border-slate-100">
               <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Total</div>
               <div class="text-2xl font-black text-slate-800">{{ requests.length }}</div>
            </div>
            <div class="p-5 rounded-3xl bg-emerald-50 border border-emerald-100">
               <div class="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-2">Validées</div>
               <div class="text-2xl font-black text-slate-800">{{ countByStatus('VALIDEE') }}</div>
            </div>
            <div class="p-5 rounded-3xl bg-amber-50 border border-amber-100">
               <div class="text-[10px] font-black text-amber-600 uppercase tracking-widest mb-2">Soumises</div>
               <div class="text-2xl font-black text-slate-800">{{ countByStatus('SOUMISE') }}</div>
            </div>
            <div class="p-5 rounded-3xl bg-rose-50 border border-rose-100">
               <div class="text-[10px] font-black text-rose-600 uppercase tracking-widest mb-2">Rejetées</div>
               <div class="text-2xl font-black text-slate-800">{{ countByStatus('REJETEE') }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Taux d'approbation -->
      <div class="lg:col-span-4 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 flex flex-col items-center justify-center p-8 text-center">
         <div class="mb-4">
            <h4 class="text-xl font-bold text-slate-800 mb-1">Efficacité Globale</h4>
            <p class="text-sm text-slate-500 font-medium">Taux d'acceptation des dossiers</p>
         </div>
         
         <div class="relative w-48 h-48 flex items-center justify-center">
            <svg class="w-full h-full" viewBox="0 0 100 100">
               <circle cx="50" cy="50" r="40" fill="none" stroke="#f1f5f9" stroke-width="12" />
               <circle 
                  cx="50" cy="50" r="40" fill="none" 
                  stroke="url(#approvalGradient)" stroke-width="12" 
                  stroke-dasharray="251.2" :stroke-dashoffset="251.2 - (251.2 * approvalRate / 100)" 
                  stroke-linecap="round" transform="rotate(-90 50 50)" class="transition-all duration-1000 ease-out"
               />
               <defs>
                  <linearGradient id="approvalGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                     <stop offset="0%" stop-color="#818cf8" />
                     <stop offset="100%" stop-color="#4f46e5" />
                  </linearGradient>
               </defs>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
               <div class="text-4xl font-black text-slate-800">{{ approvalRate }}%</div>
               <div class="text-[10px] font-black text-indigo-600 uppercase tracking-widest mt-1">Acceptation</div>
            </div>
         </div>

         <div class="mt-8 w-full space-y-4">
            <div class="flex items-center justify-between text-sm">
                <span class="font-bold text-slate-600">Dossiers Validés</span>
                <span class="font-black text-emerald-600">{{ countByStatus('VALIDEE') }}</span>
            </div>
            <div class="relative h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                <div class="absolute inset-y-0 left-0 bg-emerald-500 rounded-full" :style="{ width: approvalRate + '%' }"></div>
            </div>
            <div class="flex items-center justify-between text-sm pt-2">
                <span class="font-bold text-slate-600">Dossiers Rejetés</span>
                <span class="font-black text-rose-600">{{ countByStatus('REJETEE') }}</span>
            </div>
            <div class="relative h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                <div class="absolute inset-y-0 left-0 bg-rose-500 rounded-full" :style="{ width: (100 - approvalRate) + '%' }"></div>
            </div>
         </div>
      </div>

      <!-- Répartition par type -->
      <div class="lg:col-span-12 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 overflow-hidden">
        <div class="p-8 border-b border-slate-100">
           <h4 class="text-xl font-bold text-slate-800">Distribution par type de document</h4>
        </div>
        <div class="p-8">
           <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div v-for="type in typeStatistics" :key="type.name" class="group relative overflow-hidden p-6 rounded-3xl border-2 border-slate-50 hover:border-indigo-100 transition-all duration-300">
                  <div class="flex items-center justify-between mb-4">
                      <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-white shadow-lg" :style="{ background: type.color }">
                          <FileText class="w-6 h-6" />
                      </div>
                      <div class="text-2xl font-black text-slate-800">{{ type.count }}</div>
                  </div>
                  <h5 class="text-base font-bold text-slate-700 mb-1">{{ type.name }}</h5>
                  <div class="flex items-center justify-between">
                      <span class="text-xs text-slate-400 font-bold uppercase tracking-wider">{{ type.percentage }}% du total</span>
                  </div>
                  <div class="mt-4 h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-1000" :style="{ width: type.percentage + '%', background: type.color }"></div>
                  </div>
              </div>
           </div>
        </div>
      </div>

    </section>

  </div>
</template>

<script>
import { BarChart3, FileText, TrendingUp, Download, ChevronDown, TableProperties } from 'lucide-vue-next';
import * as XLSX from 'xlsx';

export default {
  name: 'Statistiques',
  components: { BarChart3, FileText, TrendingUp, Download, ChevronDown, TableProperties },
  props: {
    requests: { type: Array, required: true }
  },
  data() {
    return {
      exportPeriod: 'all',
      monthLabelsShort: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
      colors: ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'],
      currentYear: new Date().getFullYear()
    };
  },
  computed: {
    monthlyCounts() {
      const counts = new Array(12).fill(0);
      this.requests.forEach(req => {
        const date = new Date(req.dateDepot);
        if (date.getFullYear() === this.currentYear) {
          counts[date.getMonth()]++;
        }
      });
      return counts;
    },
    monthlyChartPoints() {
      const max = Math.max(...this.monthlyCounts, 5);
      const width = 600;
      const height = 240;
      const px = 40;
      const py = 40;
      
      return this.monthlyCounts.map((val, i) => ({
        x: px + (i * ((width - 2*px)/11)),
        y: height - py - (val * ((height - 2*py)/max)),
        val
      }));
    },
    chartLinePath() {
      if (!this.monthlyChartPoints.length) return '';
      return 'M' + this.monthlyChartPoints.map(p => `${p.x},${p.y}`).join(' L');
    },
    chartAreaPath() {
      if (!this.monthlyChartPoints.length) return '';
      const first = this.monthlyChartPoints[0];
      const last = this.monthlyChartPoints[this.monthlyChartPoints.length - 1];
      return `M${first.x},200 L${this.chartLinePath.substring(1)} L${last.x},200 Z`;
    },
    approvalRate() {
      const v = this.countByStatus('VALIDEE');
      const r = this.countByStatus('REJETEE');
      if (v + r === 0) return 0;
      return Math.round((v / (v + r)) * 100);
    },
    typeStatistics() {
      const s = {};
      this.requests.forEach(r => {
        const t = r.typeDemande || 'Inconnu';
        s[t] = (s[t] || 0) + 1;
      });
      const total = this.requests.length || 1;
      return Object.keys(s).map((name, i) => ({
        name,
        count: s[name],
        percentage: Math.round((s[name]/total)*100),
        color: this.colors[i % this.colors.length]
      })).sort((a,b) => b.count - a.count);
    }
  },
  methods: {
    countByStatus(status) {
      if (!this.requests) return 0;
      return this.requests.filter(r => r.status === status).length;
    },
    
    // EXPORT EXCEL
    exportExcel() {
      try {
        const data = this.requests.map(r => ({
          'Référence': r.reference,
          'Demandeur': r.demandeur ? `${r.demandeur.prenom} ${r.demandeur.nom}` : 'Inconnu',
          'Type': r.typeDemande,
          'Date Dépôt': new Date(r.dateDepot).toLocaleDateString('fr-FR'),
          'Statut': r.status
        }));
        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Données");
        XLSX.writeFile(wb, `Statistiques_Export_${new Date().toISOString().slice(0,10)}.xlsx`);
      } catch (err) {
        console.error(err);
        alert("Erreur lors de l'export Excel");
      }
    },
    
    // EXPORT CSV
    exportCSV() {
      try {
        const headers = "Reference,Demandeur,Type,Date,Statut\n";
        const rows = this.requests.map(r => 
          `${r.reference},${r.demandeur ? r.demandeur.nom : '?'},${r.typeDemande},${new Date(r.dateDepot).toLocaleDateString()},${r.status}`
        ).join("\n");
        const blob = new Blob([headers + rows], { type: 'text/csv' });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `Export_Data_${new Date().toISOString().slice(0,10)}.csv`;
        link.click();
      } catch (err) {
        console.error(err);
      }
    }
  }
};
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.space-y-8 { animation: fadeInUp 0.4s ease-out; }
</style>