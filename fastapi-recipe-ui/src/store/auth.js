import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api";

export const useAuthStore = defineStore("auth", () => {
  const isAuthenticated = ref(false);

  // Check if user is authenticated (via backend)
  const checkAuth = async () => {
    try {
      await api.get("/user/profile/");
      isAuthenticated.value = true;
    } catch (error) {
      isAuthenticated.value = false;
    }
  };

  // Login function
  const login = async (email, password) => {
    try {
      const formData = new URLSearchParams();
      formData.append("email", email);
      formData.append("password", password);

      await api.post("/login/", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        withCredentials: true,
      });

      isAuthenticated.value = true;
    } catch (error) {
      throw new Error("Invalid email or password");
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await api.post("/logout/", {}, { withCredentials: true });
    } catch (error) {
      console.error("Logout failed", error);
    } finally {
      isAuthenticated.value = false;
    }
  };
  return { isAuthenticated, checkAuth, login, logout };

});
