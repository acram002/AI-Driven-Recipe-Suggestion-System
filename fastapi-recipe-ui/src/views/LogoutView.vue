<script setup>
import { removeToken } from "@/utils/auth"; // import this (we'll create it)
import { useRouter } from "vue-router";
import api from "@/api"; // make sure you imported

const router = useRouter();

const logout = async () => {
  try {
    await api.post("/logout/");
    // Clear cookie/token manually if needed (optional)
    router.push("/login"); // Just push to login
  } catch (error) {
    console.error("Logout failed", error);
  }
};


</script>
