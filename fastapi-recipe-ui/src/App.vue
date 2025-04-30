<template>
  <div id="app" class="d-flex flex-column min-vh-100">
    <!-- Navbar -->
    <Navbar />

    <!-- Page Content -->
    <main class="flex-grow-1">
      <router-view />
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
// ✅ Import Navbar and Footer from components
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
/* Background for full app */
body {
  background: linear-gradient(to right, #f0f4f8, #d9e2ec, #bcccdc);
  font-family: 'Poppins', 'Roboto', sans-serif;
  color: #2f3e46;
  min-height: 100vh;
  margin: 0;
}

/* Main container should grow and push footer to bottom */
main {
  padding: 20px;
}

/* Button style */
button, .b-button {
  border-radius: 25px;
  transition: all 0.3s ease;
}

.b-button:hover {
  transform: scale(1.05);
}

/* Card style */
.card, .b-card {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-radius: 12px;
  background: white;
  padding: 20px;
  animation: fadeInUp 0.6s ease forwards;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Animations */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const auth = useAuthStore();
const router = useRouter();

onMounted(auth.checkAuth);

// Handle logout with redirection
const handleLogout = async () => {
  await auth.logout();
  router.push("/login");
};
</script>

<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/dashboard" v-if="auth.isAuthenticated">Dashboard</router-link>
    <router-link to="/profile" v-if="auth.isAuthenticated">Profile</router-link>
    <router-link to="/preferences" v-if="auth.isAuthenticated">Preferences</router-link>
    <router-link to="/login" v-if="!auth.isAuthenticated">Login</router-link>
    <router-link to="/register" v-if="!auth.isAuthenticated">Register</router-link>
    <router-link to="/history" v-if="auth.isAuthenticated">History</router-link>
    <button v-if="auth.isAuthenticated" @click="handleLogout">Logout</button>
  </nav>

  <router-view />
</template>


<style>
nav {
  padding: 10px;
}
nav a {
  margin-right: 15px;
  text-decoration: none;
  color: blue;
}
</style>
