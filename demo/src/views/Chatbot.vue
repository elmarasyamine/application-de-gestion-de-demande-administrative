<template>
  <!-- Chatbot Floating Button -->
  <div class="chatbot-container">
    <!-- Chat Window -->
    <transition name="chat-window">
      <div v-if="isOpen" class="chat-window">
        <!-- Header -->
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>
              </svg>
            </div>
            <div>
              <h3 class="chat-title">Assistant Virtuel</h3>
              <span class="chat-status">
                <span class="status-dot"></span>
                En ligne
              </span>
            </div>
          </div>
          <button @click="toggleChat" class="chat-close-btn" title="Fermer">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
            </svg>
          </button>
        </div>

        <!-- Messages -->
        <div class="chat-messages" ref="messagesContainer">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            :class="['message', msg.sender === 'user' ? 'message-user' : 'message-bot']"
          >
            <div v-if="msg.sender === 'bot'" class="bot-avatar-small">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>
              </svg>
            </div>
            <div :class="['message-bubble', msg.sender === 'user' ? 'bubble-user' : 'bubble-bot']">
              <div class="message-text" v-html="formatMessage(msg.text)"></div>
              <span class="message-time">{{ msg.time }}</span>
            </div>
          </div>

          <!-- Suggestions -->
          <div v-if="suggestions.length > 0" class="suggestions-container">
            <button
              v-for="(suggestion, index) in suggestions"
              :key="index"
              @click="sendSuggestion(suggestion)"
              class="suggestion-btn"
            >
              <component :is="getIconForSuggestion(suggestion)" class="suggestion-icon" />
              {{ suggestion }}
            </button>
          </div>

          <!-- Typing indicator -->
          <div v-if="isTyping" class="message message-bot">
            <div class="bot-avatar-small">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>
              </svg>
            </div>
            <div class="bubble-bot typing-indicator">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="chat-input-container">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Écrivez un message..."
            class="chat-input"
            :disabled="isTyping"
          />
          <button @click="sendMessage" class="chat-send-btn" :disabled="!inputMessage.trim() || isTyping">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>
            </svg>
          </button>
        </div>
      </div>
    </transition>

    <!-- Floating Button -->
    <button @click="toggleChat" :class="['chat-fab', isOpen ? 'fab-active' : '']">
      <transition name="fab-icon" mode="out-in">
        <svg v-if="!isOpen" key="chat" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>
        </svg>
        <svg v-else key="close" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
        </svg>
      </transition>
      <span v-if="!isOpen && unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
    </button>
  </div>
</template>

<script>
import { 
  MessageSquare, 
  FileText, 
  PlusCircle, 
  HelpCircle, 
  Clock, 
  Phone, 
  Search, 
  LayoutDashboard,
  Send,
  X,
  Bot
} from "lucide-vue-next";
import { sendMessage as sendChatMessage } from "../services/chatbotService";

export default {
  name: "Chatbot",
  components: {
    MessageSquare,
    FileText,
    PlusCircle,
    HelpCircle,
    Clock,
    Phone,
    Search,
    LayoutDashboard,
    Send,
    X,
    Bot
  },
  data() {
    return {
      isOpen: false,
      inputMessage: "",
      messages: [],
      suggestions: [],
      isTyping: false,
      unreadCount: 1,
    };
  },
  computed: {
    currentUser() {
      const user = localStorage.getItem("user");
      return user ? JSON.parse(user) : null;
    },
    userId() {
      return this.currentUser ? this.currentUser.id : null;
    }
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        this.unreadCount = 0;
        if (this.messages.length === 0) {
          this.addBotMessage(
            "Bonjour ! Je suis l'assistant virtuel de la plateforme.\n\nComment puis-je vous aider ?",
            ["Voir mes demandes", "Soumettre une demande", "Types de demandes", "Aide"]
          );
        }
        this.$nextTick(() => this.scrollToBottom());
      }
    },
    async sendMessage() {
      const text = this.inputMessage.trim();
      if (!text) return;

      this.addUserMessage(text);
      this.inputMessage = "";
      this.suggestions = [];
      this.isTyping = true;
      this.scrollToBottom();

      try {
        const response = await sendChatMessage(text, this.userId);
        setTimeout(() => {
          this.isTyping = false;
          this.addBotMessage(
            response.data.response,
            response.data.suggestions || []
          );
          this.scrollToBottom();
        }, 600);
      } catch (error) {
        this.isTyping = false;
        this.addBotMessage(
          "Désolé, une erreur est survenue. Veuillez réessayer.",
          ["Aide"]
        );
        this.scrollToBottom();
      }
    },
    sendSuggestion(suggestion) {
      this.inputMessage = suggestion;
      this.sendMessage();
    },
    getIconForSuggestion(text) {
      const lower = text.toLowerCase();
      if (lower.includes("voir") || lower.includes("mes demandes")) return "LayoutDashboard";
      if (lower.includes("soumettre") || lower.includes("nouvelle")) return "PlusCircle";
      if (lower.includes("types")) return "FileText";
      if (lower.includes("aide")) return "HelpCircle";
      if (lower.includes("délai") || lower.includes("temps")) return "Clock";
      if (lower.includes("contact")) return "Phone";
      return "MessageSquare";
    },
    addUserMessage(text) {
      this.messages.push({
        sender: "user",
        text: text,
        time: this.getCurrentTime()
      });
    },
    addBotMessage(text, suggestions = []) {
      this.messages.push({
        sender: "bot",
        text: text,
        time: this.getCurrentTime()
      });
      this.suggestions = suggestions;
    },
    formatMessage(text) {
      if (!text) return "";
      let formatted = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      formatted = formatted.replace(/\n/g, "<br>");
      return formatted;
    },
    getCurrentTime() {
      const now = new Date();
      return now.getHours().toString().padStart(2, "0") + ":" +
             now.getMinutes().toString().padStart(2, "0");
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    }
  }
};
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  font-family: 'Inter', -apple-system, sans-serif;
}

/* ===== Floating Action Button ===== */
.chat-fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-fab:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
}

.chat-fab.fab-active {
  background: #f43f5e;
  box-shadow: 0 4px 14px rgba(244, 63, 94, 0.4);
}

.unread-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

/* ===== Chat Window ===== */
.chat-window {
  position: absolute;
  bottom: 72px;
  right: 0;
  width: 380px;
  max-height: 580px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ===== Header ===== */
.chat-header {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-title {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
}

.chat-status {
  font-size: 11px;
  opacity: 0.9;
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
}

.chat-close-btn {
  background: transparent;
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  opacity: 0.8;
}

.chat-close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  opacity: 1;
}

/* ===== Messages ===== */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f9fafb;
  min-height: 300px;
  max-height: 400px;
}

.chat-messages::-webkit-scrollbar {
  width: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}

.message {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.message-user {
  justify-content: flex-end;
}

.bot-avatar-small {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #4f46e5;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-bottom: 2px;
}

.message-bubble {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 13.5px;
}

.bubble-user {
  background: #4f46e5;
  color: white;
  border-bottom-right-radius: 4px;
}

.bubble-bot {
  background: white;
  color: #1f2937;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #f3f4f6;
}

.message-text {
  line-height: 1.5;
}

.message-time {
  font-size: 9px;
  opacity: 0.5;
  margin-top: 4px;
  display: block;
  text-align: right;
}

/* ===== Typing Indicator ===== */
.typing-indicator {
  padding: 12px 14px;
  display: flex;
  gap: 3px;
}

.typing-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #4f46e5;
  animation: typingBounce 1.4s infinite ease-in-out both;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typingBounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

/* ===== Suggestions ===== */
.suggestions-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
}

.suggestion-btn {
  background: white;
  border: 1px solid #e5e7eb;
  color: #4b5563;
  padding: 7px 12px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.suggestion-btn:hover {
  border-color: #4f46e5;
  color: #4f46e5;
  background: #f5f3ff;
  transform: translateY(-1px);
}

.suggestion-icon {
  width: 14px;
  height: 14px;
  opacity: 0.7;
}

/* ===== Input ===== */
.chat-input-container {
  padding: 14px 18px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  gap: 8px;
  background: white;
}

.chat-input {
  flex: 1;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 9px 14px;
  font-size: 13.5px;
  outline: none;
  background: #f9fafb;
}

.chat-input:focus {
  border-color: #4f46e5;
  background: white;
}

.chat-send-btn {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #4f46e5;
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.chat-send-btn:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-1px);
}

.chat-send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ===== Transitions ===== */
.chat-window-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.chat-window-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

.chat-window-leave-active {
  transition: all 0.2s ease-in;
}

.chat-window-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}
</style>
