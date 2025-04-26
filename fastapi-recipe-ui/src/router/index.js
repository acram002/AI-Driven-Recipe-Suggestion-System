import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import Login from "@/views/LoginView.vue";
import Profile from "@/views/ProfileView.vue";
import Preferences from "@/views/PreferencesView.vue";
import Register from "@/views/RegisterView.vue";
import HistoryView from "@/views/HistoryView.vue";
import { useAuthStore } from "@/store/auth"; // ✅ use Pinia store!

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/preferences", component: Preferences, meta: { requiresAuth: true } },
  { path: "/history", component: HistoryView, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to protect routes
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore(); // 🛡️ use Pinia auth store

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    await auth.checkAuth(); // Double-check auth status from server
    if (!auth.isAuthenticated) {
      return next("/login"); // Redirect to login
    }
  }
  next();
});

export default router;
