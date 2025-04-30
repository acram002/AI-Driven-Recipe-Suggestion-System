<template>
  <button @click="logout">Logout</button>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const logout = async () => {
  try {
    await api.post("/logout/");
    router.push("/login"); // Redirect to login
  } catch (error) {
    console.error("Logout failed", error);
  }
};

</script>
