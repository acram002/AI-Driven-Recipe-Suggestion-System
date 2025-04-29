<template>
  <b-navbar toggleable="lg" type="light" variant="light" class="shadow-sm mb-4" style="background: linear-gradient(to right, #74ebd5, #ACB6E5);">
    <b-container>
      <!-- App Name -->
      <b-navbar-brand to="/" tag="router-link" class="brand-title">
        🍽️ AIRecipe
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" />

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto d-flex align-items-center justify-content-end" style="width: 100%;">
          
          <!-- Public Links -->
          <router-link to="/" class="nav-btn">🏠 Home</router-link>

          <!-- Private Links -->
          <template v-if="auth.isAuthenticated">
            <router-link to="/profile" class="nav-btn">👤 Profile</router-link>
            <router-link to="/preferences" class="nav-btn">⚙️ Preferences</router-link>
            <router-link to="/liked" class="nav-btn">❤️ Liked</router-link>
            <router-link to="/history" class="nav-btn">📜 History</router-link>
          </template>

          <!-- Guest Links -->
          <template v-else>
            <router-link to="/login" class="nav-btn btn-login">🔑 Login</router-link>
            <router-link to="/register" class="nav-btn btn-register">📝 Register</router-link>
          </template>

          <!-- Logout Button -->
          <template v-if="auth.isAuthenticated">
            <button class="nav-btn btn-logout ml-2" @click="auth.logout">
              🔴 Logout
            </button>
          </template>

        </b-navbar-nav>
      </b-collapse>
    </b-container>
  </b-navbar>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
const auth = useAuthStore()
</script>

<style scoped>
/* Brand App Name */
.brand-title {
  font-weight: bold;
  font-size: 1.8rem;
  color: #1e3a8a; /* Deep blue */
}

/* Buttons Common */
.nav-btn {
  margin-left: 12px;
  margin-bottom: 6px;
  padding: 8px 16px;
  border-radius: 25px;
  text-decoration: none;
  background: #ffffff;
  color: #364fc7;
  font-weight: 500;
  font-size: 15px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.nav-btn:hover {
  background: #dbe4ff;
  color: #1c1c3c;
  transform: translateY(-2px);
}

/* Login special */
.btn-login {
  background: #51cf66;
  color: white;
}

.btn-login:hover {
  background: #37b24d;
}

/* Register special */
.btn-register {
  background: #339af0;
  color: white;
}

.btn-register:hover {
  background: #1c7ed6;
}

/* Logout special */
.btn-logout {
  background: #ff6b6b;
  color: white;
}

.btn-logout:hover {
  background: #fa5252;
}

/* Force navbar right side alignment */
.b-navbar-nav {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>
