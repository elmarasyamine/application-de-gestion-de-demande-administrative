<template>
  <div class="min-h-screen">
    
    <!-- MESSAGING LAYOUT -->
    <div class="h-[calc(100vh-8rem)] flex gap-6">
      
      <!-- CONVERSATIONS LIST -->
      <div class="w-96 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 flex flex-col overflow-hidden">
        
        <!-- Panel Header -->
        <div class="relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-600"></div>
          <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAgTSAwIDIwIEwgNDAgMjAgTSAyMCAwIEwgMjAgNDAgTSAwIDMwIEwgNDAgMzAgTSAzMCAwIEwgMzAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-40"></div>
          
          <div class="relative z-10 px-6 py-5">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-bold text-white flex items-center gap-3">
                <MessageCircle class="w-6 h-6" />
                <span>Conversations</span>
              </h3>
              <div class="bg-white/25 backdrop-blur-sm rounded-full px-4 py-1.5 border border-white/30">
                <span class="text-sm font-black text-white">{{ conversations.length }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Search Box -->
        <div class="p-4">
          <div class="relative group">
            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <input 
              type="text" 
              placeholder="Rechercher une conversation..."
              v-model="searchQuery"
              class="w-full pl-12 pr-4 py-3.5 rounded-2xl border-2 border-slate-200 focus:border-indigo-500 focus:outline-none transition-all bg-white/80 backdrop-blur-sm font-medium text-slate-700 placeholder-slate-400"
            >
          </div>
        </div>

        <!-- Conversations List -->
        <div class="flex-1 overflow-y-auto px-3 pb-3 space-y-2 scrollbar-custom">
          <div 
            v-for="conv in filteredConversations" 
            :key="conv.id"
            @click="selectConversation(conv.id)"
            :class="[
              'group relative p-4 rounded-2xl cursor-pointer transition-all duration-300',
              selectedConv === conv.id 
                ? 'bg-gradient-to-r from-indigo-100 to-violet-100 shadow-lg' 
                : 'hover:bg-slate-50 hover:shadow-md'
            ]"
          >
            <!-- Unread indicator line -->
            <div 
              v-if="conv.unread > 0"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-12 rounded-full bg-gradient-to-b from-indigo-500 to-violet-600"
            ></div>
            
            <div class="flex items-start gap-3">
              <!-- Avatar -->
              <div class="relative flex-shrink-0">
                <div 
                  :class="[
                    'w-12 h-12 rounded-2xl flex items-center justify-center text-white font-black text-lg shadow-md',
                    selectedConv === conv.id 
                      ? 'bg-gradient-to-br from-indigo-600 to-violet-700' 
                      : 'bg-gradient-to-br from-slate-400 to-slate-600'
                  ]"
                >
                  {{ conv.name.charAt(0) }}
                </div>
                <!-- Online status -->
                <div class="absolute -bottom-0.5 -right-0.5 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
              </div>

              <!-- Conversation Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <h4 
                    :class="[
                      'font-bold truncate',
                      conv.unread > 0 ? 'text-slate-900' : 'text-slate-700'
                    ]"
                  >
                    {{ conv.name }}
                  </h4>
                  <span class="text-xs font-medium text-slate-500 flex-shrink-0 ml-2">
                    {{ conv.lastMessage }}
                  </span>
                </div>
                
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-xs font-mono font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-lg">
                    {{ conv.ref }}
                  </span>
                </div>

                <p 
                  :class="[
                    'text-sm truncate',
                    conv.unread > 0 ? 'text-slate-700 font-semibold' : 'text-slate-500'
                  ]"
                >
                  {{ conv.lastMessageText }}
                </p>
              </div>

              <!-- Unread Badge -->
              <div 
                v-if="conv.unread > 0" 
                class="flex-shrink-0 ml-2"
              >
                <div class="w-6 h-6 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                  <span class="text-xs font-black text-white">{{ conv.unread }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-if="filteredConversations.length === 0" class="flex flex-col items-center justify-center py-12 px-4">
            <div class="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
              <Search class="w-12 h-12 text-slate-400" />
            </div>
            <p class="text-slate-500 font-medium text-center">Aucune conversation trouvée</p>
          </div>
        </div>
      </div>

      <!-- CHAT AREA -->
      <div class="flex-1 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 flex flex-col overflow-hidden">
        
        <!-- Empty State -->
        <div v-if="!selectedConv" class="flex-1 flex flex-col items-center justify-center">
          <div class="relative mb-8">
            <div class="w-32 h-32 rounded-3xl bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-br from-indigo-100/30 to-violet-100/30"></div>
              <span class="text-6xl relative z-10">💬</span>
            </div>
            <div class="absolute -top-2 -right-2 w-8 h-8 bg-violet-400 rounded-full animate-bounce"></div>
          </div>
          
          <h3 class="text-3xl font-bold text-slate-800 mb-3">Bienvenue dans la Messagerie</h3>
          <p class="text-slate-600 font-medium text-center max-w-md">
            Sélectionnez une conversation dans la liste pour commencer à échanger avec vos utilisateurs
          </p>
        </div>

        <!-- Active Chat -->
        <div v-else class="flex-1 flex flex-col h-full">
          
          <!-- Chat Header -->
          <div class="relative overflow-hidden flex-shrink-0">
            <div class="absolute inset-0 bg-gradient-to-r from-slate-50 to-indigo-50"></div>
            
            <div class="relative z-10 px-6 py-4 flex items-center justify-between border-b-2 border-slate-100">
              <div class="flex items-center gap-4">
                <!-- Avatar -->
                <div class="relative">
                  <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-700 flex items-center justify-center text-white font-black text-xl shadow-lg shadow-indigo-500/30">
                    {{ currentChat.name.charAt(0) }}
                  </div>
                  <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-pulse"></div>
                </div>

                <!-- User Info -->
                <div>
                  <h4 class="text-xl font-bold text-slate-800">{{ currentChat.name }}</h4>
                  <div class="flex items-center gap-2 text-sm">
                    <span class="font-mono font-bold text-indigo-600">{{ currentChat.ref }}</span>
                    <span class="text-slate-400">•</span>
                    <span class="font-medium text-slate-600">{{ currentChat.type }}</span>
                  </div>
                </div>
              </div>

              <!-- Action Button -->
              <button 
                @click="viewRequest(currentChat.requestId)"
                class="group flex items-center gap-3 px-5 py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-bold shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 transition-all duration-300 hover:scale-105 active:scale-95"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                <span>Voir la demande</span>
              </button>
            </div>
          </div>

          <!-- Messages Area -->
          <div 
            ref="chatMessages" 
            class="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-br from-slate-50/50 via-indigo-50/30 to-violet-50/30 scrollbar-custom"
          >
            <div 
              v-for="(msg, index) in currentChat.messages" 
              :key="index"
              :class="[
                'flex',
                msg.type === 'admin' ? 'justify-end' : 'justify-start'
              ]"
              :style="{ animationDelay: `${index * 0.05}s` }"
            >
              <div 
                :class="[
                  'max-w-xl group animate-slide-up',
                  msg.type === 'admin' ? 'items-end' : 'items-start'
                ]"
              >
                <!-- Message Bubble -->
                <div 
                  :class="[
                    'relative px-5 py-3.5 rounded-2xl shadow-md',
                    msg.type === 'admin' 
                      ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-tr-sm' 
                      : 'bg-white text-slate-800 rounded-tl-sm border-2 border-slate-100'
                  ]"
                >
                  <!-- Decorative corner -->
                  <div 
                    :class="[
                      'absolute w-3 h-3',
                      msg.type === 'admin' 
                        ? 'top-0 right-0 bg-violet-600' 
                        : 'top-0 left-0 bg-white border-l-2 border-t-2 border-slate-100'
                    ]"
                  ></div>

                  <p class="text-sm font-medium leading-relaxed relative z-10">{{ msg.text }}</p>
                  
                  <!-- Time -->
                  <div 
                    :class="[
                      'text-xs font-semibold mt-2 flex items-center gap-2',
                      msg.type === 'admin' ? 'text-indigo-200 justify-end' : 'text-slate-400 justify-start'
                    ]"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>{{ msg.time }}</span>
                  </div>
                </div>

                <!-- Read receipt (for admin messages) -->
                <div 
                  v-if="msg.type === 'admin'" 
                  class="flex items-center gap-1 mt-1 px-2"
                >
                  <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span class="text-xs font-semibold text-slate-500">Lu</span>
                </div>
              </div>
            </div>

            <!-- Typing indicator -->
            <div v-if="isTyping" class="flex justify-start animate-pulse">
              <div class="bg-white border-2 border-slate-100 rounded-2xl rounded-tl-sm px-5 py-3 shadow-md">
                <div class="flex items-center gap-1.5">
                  <div class="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style="animation-delay: 0s"></div>
                  <div class="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style="animation-delay: 0.2s"></div>
                  <div class="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="flex-shrink-0 p-6 bg-white/80 backdrop-blur-sm border-t-2 border-slate-100">
            <div class="flex items-end gap-3">
              <!-- Attachment button -->
              <button class="group w-12 h-12 rounded-2xl bg-slate-100 hover:bg-slate-200 flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95">
                <svg class="w-6 h-6 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"></path>
                </svg>
              </button>

              <!-- Message Input -->
              <div class="flex-1 relative">
                <textarea
                  v-model="newMessage"
                  @keypress.enter.exact.prevent="sendMessage"
                  placeholder="Tapez votre message... (Entrée pour envoyer)"
                  rows="1"
                  class="w-full px-5 py-3.5 rounded-2xl border-2 border-slate-200 focus:border-indigo-500 focus:outline-none transition-all bg-white font-medium text-slate-700 placeholder-slate-400 resize-none scrollbar-custom"
                  style="min-height: 48px; max-height: 120px;"
                ></textarea>
              </div>

              <!-- Emoji button -->
              <button class="group w-12 h-12 rounded-2xl bg-slate-100 hover:bg-slate-200 flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95">
                <span class="text-2xl group-hover:scale-125 transition-transform">😊</span>
              </button>

              <!-- Send Button -->
              <button 
                @click="sendMessage"
                :disabled="!newMessage.trim()"
                :class="[
                  'group w-12 h-12 rounded-2xl flex items-center justify-center font-bold transition-all duration-300 shadow-lg',
                  newMessage.trim() 
                    ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 hover:scale-110 active:scale-95' 
                    : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                ]"
              >
                <svg class="w-6 h-6 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
              </button>
            </div>

            <!-- Quick Responses (optional) -->
            <div class="flex items-center gap-2 mt-3">
              <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">Réponses rapides:</span>
              <button 
                v-for="quick in quickResponses" 
                :key="quick"
                @click="newMessage = quick"
                class="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-indigo-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-all hover:scale-105"
              >
                {{ quick }}
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { MessageCircle, Search } from 'lucide-vue-next';

export default {
  name: 'Messagerie',
  components: { MessageCircle, Search },
  props: {
    requests: { type: Array, required: true }
  },
  data() {
    return {
      selectedConv: null,
      newMessage: '',
      searchQuery: '',
      conversations: [
        { 
          id: 1, 
          name: 'Ahmed Ali', 
          ref: 'REQ001', 
          type: 'Attestation',
          requestId: 1,
          lastMessage: 'Il y a 5 min', 
          lastMessageText: 'Merci beaucoup pour votre aide',
          unread: 2,
          messages: [
            { type: 'received', text: 'Bonjour, j\'ai besoin d\'une attestation de scolarité', time: '10:30' },
            { type: 'sent', text: 'Bonjour Ahmed, votre demande est en cours de traitement', time: '10:35' },
            { type: 'received', text: 'Combien de temps cela prendra ?', time: '10:40' },
            { type: 'sent', text: 'Environ 2-3 jours ouvrables', time: '10:45' },
            { type: 'received', text: 'Merci beaucoup pour votre aide', time: '10:50' }
          ]
        },
        { 
          id: 2, 
          name: 'Sara Ben', 
          ref: 'REQ002', 
          type: 'Certificat',
          requestId: 2,
          lastMessage: 'Il y a 1h', 
          lastMessageText: 'D\'accord, merci',
          unread: 0,
          messages: [
            { type: 'received', text: 'Bonjour, ma demande a-t-elle été validée ?', time: '09:15' },
            { type: 'sent', text: 'Oui, votre certificat est prêt', time: '09:20' },
            { type: 'received', text: 'Où puis-je le récupérer ?', time: '09:25' },
            { type: 'sent', text: 'Au bureau de la scolarité, bâtiment A', time: '09:30' },
            { type: 'received', text: 'D\'accord, merci', time: '09:35' }
          ]
        },
        { 
          id: 3, 
          name: 'Karim Zaki', 
          ref: 'REQ003', 
          type: 'Attestation',
          requestId: 3,
          lastMessage: 'Il y a 2h', 
          lastMessageText: 'Merci pour l\'information',
          unread: 1,
          messages: [
            { type: 'received', text: 'Bonjour, quand puis-je obtenir mon attestation ?', time: '08:00' },
            { type: 'sent', text: 'Bonjour, nous traitons votre demande actuellement', time: '08:15' },
            { type: 'received', text: 'Merci pour l\'information', time: '08:20' }
          ]
        },
        { 
          id: 4, 
          name: 'Fatima Nour', 
          ref: 'REQ004', 
          type: 'Justificatif',
          requestId: 4,
          lastMessage: 'Hier', 
          lastMessageText: 'Je vais le refaire',
          unread: 0,
          messages: [
            { type: 'sent', text: 'Votre demande a été rejetée car il manque des documents', time: 'Hier 14:30' },
            { type: 'received', text: 'Quels documents exactement ?', time: 'Hier 15:00' },
            { type: 'sent', text: 'La signature du tuteur et le cachet de l\'entreprise', time: 'Hier 15:15' },
            { type: 'received', text: 'Je vais le refaire', time: 'Hier 15:30' }
          ]
        },
        { 
          id: 5, 
          name: 'Omar Hassan', 
          ref: 'REQ005', 
          type: 'Certificat',
          requestId: 5,
          lastMessage: 'Hier', 
          lastMessageText: 'Parfait !',
          unread: 0,
          messages: [
            { type: 'sent', text: 'Votre certificat est prêt', time: 'Hier 16:00' },
            { type: 'received', text: 'Parfait !', time: 'Hier 16:05' }
          ]
        },
        { 
          id: 6, 
          name: 'Yasmine Idrissi', 
          ref: 'REQ006', 
          type: 'Attestation',
          requestId: 6,
          lastMessage: 'Il y a 3h', 
          lastMessageText: 'C\'est urgent pour moi',
          unread: 3,
          messages: [
            { type: 'received', text: 'Bonjour, j\'ai besoin de mon attestation rapidement', time: '07:00' },
            { type: 'received', text: 'C\'est urgent pour moi', time: '07:05' }
          ]
        }
      ]
    };
  },
  computed: {
    filteredConversations() {
      if (!this.searchQuery) return this.conversations;
      return this.conversations.filter(conv => 
        conv.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        conv.ref.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    currentChat() {
      return this.conversations.find(c => c.id === this.selectedConv) || null;
    }
  },
  methods: {
    selectConversation(id) {
      this.selectedConv = id;
      // Marquer comme lu
      const conv = this.conversations.find(c => c.id === id);
      if (conv) conv.unread = 0;
      this.$nextTick(() => this.scrollToBottom());
    },
    sendMessage() {
      if (!this.newMessage.trim() || !this.selectedConv) return;
      
      const conv = this.conversations.find(c => c.id === this.selectedConv);
      if (!conv) return;
      
      const now = new Date();
      const time = now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      
      conv.messages.push({
        type: 'sent',
        text: this.newMessage,
        time: time
      });
      
      conv.lastMessage = 'À l\'instant';
      conv.lastMessageText = this.newMessage;
      
      this.newMessage = '';
      this.$nextTick(() => this.scrollToBottom());
    },
    scrollToBottom() {
      const chatMessages = this.$refs.chatMessages;
      if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    },
    viewRequest(requestId) {
      this.$router.push(`/admin/demande/${requestId}`);
    }
  }
};
</script>

<style scoped>
.messagerie-admin {
  padding: 32px;
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.messaging-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 20px;
  height: calc(100vh - 150px);
}

/* CONVERSATIONS PANEL */
.conversations-panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.panel-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 700;
}

.conv-count {
  background: white;
  color: #667eea;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

.search-conversations {
  position: relative;
  padding: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.search-conversations .search-icon {
  position: absolute;
  left: 28px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
}

.search-input {
  width: 100%;
  padding: 10px 10px 10px 35px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.conversation-item:hover {
  background: #f9fafb;
}

.conversation-item.active {
  background: #eff6ff;
  border-left: 4px solid #667eea;
}

.conv-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 18px;
  flex-shrink: 0;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-name {
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
  font-size: 14px;
}

.conv-ref {
  font-size: 12px;
  color: #667eea;
  font-weight: 600;
  margin-bottom: 4px;
}

.conv-preview {
  font-size: 13px;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.conv-time {
  font-size: 11px;
  color: #9ca3af;
}

.conv-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

/* CHAT PANEL */
.chat-panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chat-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.chat-placeholder p {
  font-size: 16px;
  font-weight: 500;
}

.chat-active {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-avatar {
  width: 42px;
  height: 42px;
  background: white;
  color: #667eea;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.chat-title h4 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.chat-ref {
  font-size: 12px;
  opacity: 0.9;
}

.btn-view-request {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-view-request:hover {
  background: #f3f4f6;
  transform: translateY(-2px);
}

.chat-messages {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #f9fafb;
}

.message {
  display: flex;
  animation: messageSlide 0.3s ease;
}

@keyframes messageSlide {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-received {
  justify-content: flex-start;
}

.message-sent {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
}

.message-received .message-bubble {
  background: white;
  color: #1f2937;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-sent .message-bubble {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.message-text {
  margin-bottom: 6px;
  line-height: 1.5;
  font-size: 14px;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
}

.chat-input-area {
  padding: 20px 24px;
  border-top: 2px solid #e5e7eb;
  display: flex;
  gap: 12px;
  background: white;
}

.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-send {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.btn-send:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* SCROLLBAR */
.conversations-list::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.conversations-list::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track {
  background: #f3f4f6;
}

.conversations-list::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.conversations-list::-webkit-scrollbar-thumb:hover,
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .messagerie-admin { padding: 20px; }
  .messaging-layout { 
    grid-template-columns: 1fr; 
    height: calc(100vh - 100px);
  }
  .conversations-panel { 
    display: none; 
  }
  .conversations-panel.mobile-show {
    display: flex;
  }
}
</style>