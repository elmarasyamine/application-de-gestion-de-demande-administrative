<template>
  <router-view />
  <Chatbot v-if="isLoggedIn" />
</template>
<script>
import Chatbot from "./views/Chatbot.vue";

export default {
  name: "App",
  components: {
    Chatbot
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user");
    }
  }
}
</script>
