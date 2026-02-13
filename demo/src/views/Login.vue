
<template>
  <div
    class="min-h-screen flex items-center justify-center
           bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800"
  >
    <!-- Card -->
    <div
      class="w-full max-w-md bg-white rounded-2xl shadow-2xl
             px-8 py-10"
      <!-- Title -->
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">
        Connexion
      </h2>
      
      <p class="text-center text-gray-500 mb-8">
        Accédez à votre espace
      </p>

      <!-- Form -->
      <form @submit.prevent="login" class="space-y-5">
        <!-- Email -->
        <div>
          <input
            type="email"
            v-model="email"
            placeholder="Email"
            required
            class="w-full px-4 py-3 rounded-xl border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-indigo-500
                   focus:border-indigo-500 transition"
          />
        </div>

        <!-- Password -->
        <div>
          <input
            type="password"
            v-model="password"
            placeholder="Mot de passe"
            required
            class="w-full px-4 py-3 rounded-xl border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-indigo-500
                   focus:border-indigo-500 transition"
          />
        </div>

        <!-- Button -->
        <button
          type="submit"
          :disabled="loading"
          :class="[
            'w-full py-3 rounded-xl text-white font-semibold text-lg transition-all duration-200',
            loading 
              ? 'bg-indigo-400 cursor-not-allowed' 
              : 'bg-indigo-600 hover:bg-indigo-700 active:scale-[0.98]'
          ]"
        >
          <span v-if="loading" class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Connexion en cours...
          </span>
          <span v-else>Se connecter</span>
        </button>
      </form>

      <!-- Register -->
      <p class="mt-6 text-center text-sm text-gray-600">
        Pas de compte ?
        <router-link
          to="/register"
          class="text-indigo-600 font-semibold hover:underline"
        >
          Créer un compte
        </router-link>
      </p>

      <!-- Error -->
      <p
        v-if="error"
        class="mt-4 text-center text-sm text-red-600 font-medium"
      >
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script>
import { login } from "../services/authService";

export default {
  name: "Login",

  data() {
    return {
      email: "",
      password: "",
      error: "",
      loading: false
    };
  },

  methods: {
    async login() {
      this.error = "";
      this.loading = true;

      // Validation côté client
      if (!this.email || !this.password) {
        this.error = "Veuillez remplir tous les champs";
        this.loading = false;
        return;
      }

      try {
        // Appel au backend pour vérifier les credentials
        const utilisateur = await login(this.email, this.password);

        // Vérifier si l'utilisateur est retourné
        if (!utilisateur || !utilisateur.id) {
          this.error = "Email ou mot de passe incorrect";
          this.loading = false;
          return;
        }

        // Stocker l'utilisateur dans localStorage
        localStorage.setItem("user", JSON.stringify(utilisateur));

        // Redirection basée sur le type d'utilisateur
        const userType = (utilisateur.type || "").toLowerCase();

        if (userType === "administrateur" || userType === "admin") {
          // Rediriger vers l'espace administrateur
          this.$router.push("/admin/tableau-de-bord");
        } else if (userType === "demandeur") {
          // Rediriger vers l'espace demandeur
          this.$router.push("/demandeur/tableau-de-bord");
        } else {
          // Type non reconnu - rediriger vers demandeur par défaut
          console.warn("Type utilisateur non reconnu:", utilisateur.type);
          this.$router.push("/demandeur/tableau-de-bord");
        }

      } catch (err) {
        console.error("Erreur de connexion:", err);
        
        // Gérer les différentes erreurs
        if (err.response) {
          // Erreur HTTP du backend
          if (err.response.status === 401) {
            this.error = "Email ou mot de passe incorrect";
          } else if (err.response.status === 404) {
            this.error = "Utilisateur non trouvé";
          } else if (err.response.data && err.response.data.message) {
            this.error = err.response.data.message;
          } else {
            this.error = "Erreur de connexion. Veuillez réessayer.";
          }
        } else if (err.request) {
          // Pas de réponse du serveur
          this.error = "Impossible de contacter le serveur. Vérifiez que le backend est en marche.";
        } else {
          this.error = err.message || "Erreur de connexion";
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

