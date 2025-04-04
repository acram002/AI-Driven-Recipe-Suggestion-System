import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import Login from "@/views/LoginView.vue";
import Profile from "@/views/ProfileView.vue";
import Preferences from "@/views/PreferencesView.vue";
import Register from "@/views/RegisterView.vue";
import { isAuthenticated } from "@/utils/auth"; // Import the new authentication check

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/preferences", component: Preferences, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to protect routes
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const loggedIn = await isAuthenticated();
    if (!loggedIn) {
      return next("/login"); // Redirect to login if not authenticated
    }
  }
  next();
});

export default router;
