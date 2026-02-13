<template>
  <div class="h-screen flex flex-col p-6 bg-gray-50">
    
    <!-- MESSAGING LAYOUT -->
    <div class="flex-1 flex gap-6 overflow-hidden">
      
      <!-- CONVERSATIONS LIST -->
      <div class="w-96 bg-white rounded-2xl shadow-xl border border-gray-100 flex flex-col overflow-hidden">
        <!-- Panel Header -->
        <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50">
          <div class="flex items-center justify-between">
            <h3 class="text-2xl font-bold text-gray-800 flex items-center gap-3">
              <span v-html="getIcon('MessageSquare', 28)" class="text-indigo-600"></span>
              <span>Conversations</span>
            </h3>
            <div class="bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full shadow-md">
              <span class="text-lg font-bold text-indigo-600">{{ conversations.length }}</span>
            </div>
          </div>
        </div>
        
        <!-- Conversations List -->
        <div class="flex-1 overflow-y-auto p-3 space-y-2">
          <div 
            v-for="conv in conversations" 
            :key="conv.requestId"
            :class="[
              'p-4 rounded-xl cursor-pointer transition-all border-2',
              selectedConversation === conv.requestId 
                ? 'bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-500 shadow-lg scale-105' 
                : 'bg-white border-gray-200 hover:border-indigo-300 hover:shadow-md'
            ]"
            @click="selectConversation(conv.requestId)"
          >
            <div class="flex items-start gap-3">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-400 to-purple-600 flex items-center justify-center shadow-md flex-shrink-0">
                <span v-html="getIcon('FileText', 24)" class="text-white"></span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <div class="font-bold text-indigo-600 font-mono text-sm">{{ conv.ref }}</div>
                  <span v-if="conv.unread" class="w-6 h-6 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                    {{ conv.unread }}
                  </span>
                </div>
                <div class="text-sm font-semibold text-gray-800 mb-1 truncate">{{ conv.type }}</div>
                <div class="text-xs text-gray-500 truncate">{{ conv.lastMessage }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CHAT AREA -->
      <div class="flex-1 bg-white rounded-2xl shadow-xl border border-gray-100 flex flex-col overflow-hidden">
        
        <!-- Placeholder when no conversation selected -->
        <div v-if="!selectedConversation" class="flex-1 flex flex-col items-center justify-center p-8">
          <div class="w-32 h-32 bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 rounded-full flex items-center justify-center mb-6 shadow-lg">
            <span v-html="getIcon('MessageCircle', 64)" class="text-indigo-500"></span>
          </div>
          <h3 class="text-2xl font-bold text-gray-800 mb-2">Messagerie</h3>
          <p class="text-gray-500 text-lg text-center">Sélectionnez une conversation pour commencer à échanger</p>
        </div>

        <!-- Active Chat -->
        <div v-else class="flex-1 flex flex-col">
          <!-- Chat Header -->
          <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-400 to-purple-600 flex items-center justify-center shadow-md">
                <span v-html="getIcon('FileText', 24)" class="text-white"></span>
              </div>
              <div>
                <h4 class="text-xl font-bold text-gray-800">{{ currentChat.title }}</h4>
                <span class="text-sm font-mono text-indigo-600 font-semibold">{{ currentChat.ref }}</span>
              </div>
            </div>
          </div>

          <!-- Chat Messages -->
          <div ref="chatMessages" class="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-br from-gray-50 to-indigo-50/30">
            <div 
              v-for="(msg, index) in currentChat.messages" 
              :key="index"
              :class="[
                'flex',
                msg.type === 'user' ? 'justify-end' : 'justify-start'
              ]"
            >
              <div 
                :class="[
                  'max-w-md px-5 py-3 rounded-2xl shadow-md',
                  msg.type === 'user' 
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-br-sm' 
                    : 'bg-white text-gray-800 rounded-bl-sm border-2 border-gray-200'
                ]"
              >
                <div class="font-medium mb-1">{{ msg.text }}</div>
                <div 
                  :class="[
                    'text-xs font-semibold flex items-center gap-1',
                    msg.type === 'user' ? 'text-white/80' : 'text-gray-500'
                  ]"
                >
                  <span v-html="getIcon('Clock', 12)"></span>
                  <span>{{ msg.time }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Chat Input Area -->
          <div class="p-6 border-t border-gray-200 bg-white">
            <div class="flex items-center gap-3">
              <input 
                type="text" 
                v-model="newMessage"
                @keypress.enter="sendMessage"
                placeholder="Tapez votre message..."
                class="flex-1 px-5 py-3 rounded-xl border-2 border-gray-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium shadow-sm hover:border-indigo-400"
              >
              <button 
                @click="sendMessage"
                :disabled="!newMessage.trim()"
                :class="[
                  'w-12 h-12 rounded-xl flex items-center justify-center transition-all shadow-lg',
                  newMessage.trim() 
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 hover:scale-110 cursor-pointer text-white' 
                    : 'bg-gray-300 cursor-not-allowed text-gray-500'
                ]"
              >
                <span v-html="getIcon('Send', 20)"></span>
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>


<script>
export default {
  name: 'MessagerieInterneVue',
  props: {
    requests: { type: Array, required: true },
    messagesData: { type: Array, required: true }
  },
  data() {
    return {
      selectedConversation: null,
      newMessage: '',
      // Bibliothèque d'icônes SVG
      icons: {
        MessageSquare: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" /></svg>',
        MessageCircle: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" /></svg>',
        FileText: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>',
        Clock: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        Send: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" /></svg>',
        User: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>',
        Users: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>',
        Mail: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" /></svg>',
        Inbox: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H6.911a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661z" /></svg>'
      }
    };
  },
  computed: {
    conversations() {
      return this.messagesData.map(conv => {
        const request = this.requests.find(r => r.id === conv.requestId);
        return {
          requestId: conv.requestId,
          ref: request.ref,
          type: request.typeLabel,
          lastMessage: conv.messages[conv.messages.length - 1].time,
          unread: conv.unread || 0
        };
      });
    },
    currentChat() {
      if (!this.selectedConversation) return null;
      const request = this.requests.find(r => r.id === this.selectedConversation);
      const conversation = this.messagesData.find(m => m.requestId === this.selectedConversation);
      return {
        title: request.typeLabel,
        ref: request.ref,
        messages: conversation.messages
      };
    }
  },
  methods: {
    getIcon(name, size = 24) {
      const icon = this.icons[name] || this.icons['MessageSquare'];
      return icon.replace('stroke-width="2"', `stroke-width="2" width="${size}" height="${size}"`);
    },
    
    selectConversation(requestId) {
      this.selectedConversation = requestId;
      // Marquer les messages comme lus
      const conversation = this.messagesData.find(m => m.requestId === requestId);
      if (conversation) {
        conversation.unread = 0;
      }
      this.$nextTick(() => this.scrollToBottom());
    },
    
    sendMessage() {
      if (!this.newMessage.trim() || !this.selectedConversation) return;
      const conversation = this.messagesData.find(m => m.requestId === this.selectedConversation);
      if (!conversation) return;
      conversation.messages.push({
        type: 'user',
        text: this.newMessage,
        time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      });
      this.newMessage = '';
      this.$nextTick(() => this.scrollToBottom());
    },
    
    scrollToBottom() {
      const chatMessages = this.$refs.chatMessages;
      if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }
};
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes messageSlide {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.flex-1.flex.flex-col > div {
  animation: messageSlide 0.3s ease;
}

/* Scrollbar personnalisé */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@media (max-width: 768px) {
  .w-96 {
    display: none;
  }
}
</style>