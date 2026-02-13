<template>
  <div
    class="min-h-screen flex items-center justify-center
           bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800"
  >
    <!-- Card -->
    <div
      class="w-full max-w-md bg-white rounded-2xl shadow-2xl
             px-8 py-10"
    >
      <!-- Title -->
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">
        Créer un compte
      </h2>
      
      <p class="text-center text-gray-500 mb-8">
        Remplissez le formulaire ci-dessous
      </p>

      <!-- Form -->
      <form @submit.prevent="createAccount" class="space-y-5">
        <!-- Prénom -->
        <div>
          <input
            type="text"
            v-model="prenom"
            placeholder="Prénom"
            required
            class="w-full px-4 py-3 rounded-xl border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-indigo-500
                   focus:border-indigo-500 transition"
          />
        </div>

        <!-- Nom -->
        <div>
          <input
            type="text"
            v-model="nom"
            placeholder="Nom"
            required
            class="w-full px-4 py-3 rounded-xl border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-indigo-500
                   focus:border-indigo-500 transition"
          />
        </div>

        <!-- CNI -->
        <div>
          <input
            type="text"
            v-model="cni"
            placeholder="CNI"
            required
            class="w-full px-4 py-3 rounded-xl border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-indigo-500
                   focus:border-indigo-500 transition"
          />
        </div>

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
          class="w-full py-3 rounded-xl bg-indigo-600 text-white
                 font-semibold text-lg hover:bg-indigo-700
                 active:scale-[0.98] transition-all duration-200"
        >
          Créer le compte
        </button>
      </form>

      <!-- Login Link -->
      <p class="mt-6 text-center text-sm text-gray-600">
        Déjà un compte ?
        <router-link
          to="/login"
          class="text-indigo-600 font-semibold hover:underline"
        >
          Se connecter
        </router-link>
      </p>

      <!-- Messages -->
      <p
        v-if="message"
        class="mt-4 text-center text-sm text-green-600 font-medium"
      >
        {{ message }}
      </p>

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
import api from "@/services/api";

export default {
  name: "Register",
  data() {
    return {
      prenom: "",
      nom: "",
      cni: "",
      email: "",
      password: "",
      message: "",
      error: ""
    };
  },
  methods: {
    async createAccount() {
      try {
        const response = await api.post("/auth/register", {
          prenom: this.prenom,
          nom: this.nom,
          cni: this.cni,
          email: this.email,
          password: this.password
        });

        console.log("Réponse backend :", response.data);

        this.message = "Compte créé avec succès 🎉";

        setTimeout(() => {
          this.$router.push("/login");
        }, 1500);

      } catch (err) {
        console.error(err);
        this.error = "Erreur lors de la création du compte ❌";
      }
    }
  }
};
</script>
