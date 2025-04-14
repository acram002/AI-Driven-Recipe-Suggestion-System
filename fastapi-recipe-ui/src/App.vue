<template>

  <nav>

    <router-link to="/">Home</router-link>
    <router-link to="/dashboard" v-if="auth.isAuthenticated">Dashboard</router-link>
    <router-link to="/profile" v-if="auth.isAuthenticated">Profile</router-link>
    <router-link to="/preferences" v-if="auth.isAuthenticated">Preferences</router-link>
    <router-link to="/login" v-if="!auth.isAuthenticated">Login</router-link>
    <router-link to="/register" v-if="!auth.isAuthenticated">Register</router-link>
    <router-link to="/history" v-if="auth.isAuthenticated">History</router-link>
    <button v-if="auth.isAuthenticated" @click="auth.logout">Logout</button>

  </nav>

  <router-view />

</template>

<script setup>

import { onMounted } from "vue";
import { useAuthStore } from "@/store/auth";

const auth = useAuthStore();

onMounted(auth.checkAuth);

</script>

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
