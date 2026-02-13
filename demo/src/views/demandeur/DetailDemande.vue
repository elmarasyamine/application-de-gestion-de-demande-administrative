<template>
  <div class="detail-page">
    <div class="page-header">
      <button class="btn-back" @click="$router.push('/demandeur/mes-demandes')">
        <span>←</span> Retour
      </button>
      <h1>Détails de la demande</h1>
    </div>

    <div class="detail-grid" v-if="request">
      <div class="detail-card">
        <h2>Informations générales</h2>
        <div class="detail-info">
          <div class="info-row">
            <span class="info-label">Référence:</span>
            <span class="info-value">{{ request.ref }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Type:</span>
            <span class="info-value">{{ request.typeLabel }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Date de dépôt:</span>
            <span class="info-value">{{ formatDate(request.date) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Statut:</span>
            <span class="info-value">
              <span class="status-badge" :class="`status-${request.status}`">
                {{ request.statusLabel }}
              </span>
            </span>
          </div>
          <div class="info-row">
            <span class="info-label">Description:</span>
            <span class="info-value">{{ request.description }}</span>
          </div>
        </div>

        <div class="detail-actions">
          <button class="btn btn-primary" @click="$router.push('/demandeur/messagerie')">
            <span>💬</span> Messagerie
          </button>
          <button 
            class="btn btn-danger" 
            v-if="request.status === 'en_attente'"
            @click="confirmCancelRequest"
          >
            <span>❌</span> Annuler la demande
          </button>
        </div>
      </div>

      <div class="detail-card">
        <h2>Historique du statut</h2>
        <div class="timeline">
          <div 
            v-for="(item, index) in request.history" 
            :key="index"
            class="timeline-item"
            :class="{ completed: index < request.history.length - 1 }"
          >
            <div class="timeline-date">{{ item.date }}</div>
            <div class="timeline-title">{{ item.status }}</div>
            <div class="timeline-desc">{{ item.desc }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DetailDemandeVue',
  props: {
    requests: {
      type: Array,
      required: true
    },
    id: {
      type: String,
      required: true
    }
  },
  computed: {
    request() {
      return this.requests.find(r => r.id === parseInt(this.id));
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    confirmCancelRequest() {
      this.$emit('cancel-request', this.request.id);
    }
  }
};
</script>

<style scoped>
.detail-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  margin-top: 1rem;
  color: #1e293b;
}

.btn-back {
  background: #f8fafc;
  color: #1e293b;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  transition: 0.3s;
}

.btn-back:hover {
  background: #e2e8f0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.detail-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 2rem;
}

.detail-card h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #1e293b;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.info-label {
  font-weight: 500;
  color: #64748b;
}

.info-value {
  font-weight: 500;
  color: #1e293b;
  text-align: right;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
}

.status-en_attente {
  background: #fef3c7;
  color: #92400e;
}

.status-en_cours {
  background: #dbeafe;
  color: #1e40af;
}

.status-validee {
  background: #d1fae5;
  color: #065f46;
}

.status-rejetee {
  background: #fee2e2;
  color: #991b1b;
}

.detail-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: 0.3s;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
  transform: translateY(-2px);
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e2e8f0;
}

.timeline-item {
  position: relative;
  padding-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -1.5rem;
  top: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #3b82f6;
  border: 3px solid #ffffff;
  box-shadow: 0 0 0 2px #3b82f6;
}

.timeline-item.completed::before {
  background: #10b981;
  box-shadow: 0 0 0 2px #10b981;
}

.timeline-date {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.timeline-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #1e293b;
}

.timeline-desc {
  font-size: 0.875rem;
  color: #64748b;
}

/* Responsive */
@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .detail-card {
    padding: 1.5rem;
  }
}
</style>