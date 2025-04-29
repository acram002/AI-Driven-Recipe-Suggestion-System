<<<<<<< HEAD
<script setup>
import { removeToken } from "@/utils/auth"; // import this (we'll create it)
import { useRouter } from "vue-router";
import api from "@/api"; // make sure you imported
=======
<template>
  <button @click="logout">Logout</button>
</template>

<script setup>
import { useRouter } from "vue-router";
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)

const router = useRouter();

const logout = async () => {
  try {
    await api.post("/logout/");
<<<<<<< HEAD
    // Clear cookie/token manually if needed (optional)
    router.push("/login"); // Just push to login
=======
    router.push("/login"); // Redirect to login
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
  } catch (error) {
    console.error("Logout failed", error);
  }
};

<<<<<<< HEAD

=======
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
</script>
