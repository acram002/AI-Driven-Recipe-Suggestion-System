import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import Login from "@/views/LoginView.vue";
import Profile from "@/views/ProfileView.vue";
import Preferences from "@/views/PreferencesView.vue";
import Register from "@/views/RegisterView.vue";
import HistoryView from "@/views/HistoryView.vue";
import LikedRecipesView from "@/views/LikedRecipesView.vue";
import DislikedRecipesView from "@/views/DislikedRecipesView.vue";
import { useAuthStore } from "@/store/auth"; // ✅ using Pinia

const routes = [
  { path: "/", component: Home, meta: { requiresAuth: true } }, // 🛡 PROTECTED now
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/preferences", component: Preferences, meta: { requiresAuth: true } },
  { path: "/history", component: HistoryView, meta: { requiresAuth: true } },
  { path: "/liked", component: LikedRecipesView, meta: { requiresAuth: true } },
  { path: "/disliked", component: DislikedRecipesView, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 🛡 Navigation guard with Pinia-based auth check
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    await auth.checkAuth(); // ✅ Double-check auth from server
    if (!auth.isAuthenticated) {
      return next("/login");
    }
  }

  next();
});

export default router;
