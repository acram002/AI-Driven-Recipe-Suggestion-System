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
