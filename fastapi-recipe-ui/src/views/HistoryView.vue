<script setup>
import { BCard, BTable } from 'bootstrap-vue-next';
</script>

<template>
  <div class="container mt-4">
    <b-card>
      <h2>User Recipe Suggestion History</h2>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <b-table :items="history" :fields="fields" striped hover responsive></b-table>
      </div>
    </b-card>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "HistoryView",
  data() {
    return {
      history: [],
      loading: true,
      fields: [
        { key: "title", label: "Recipe Title" },
        { key: "description", label: "Description" },
        { key: "ingredients_used", label: "Ingredients Used" },
        { key: "suggested_at", label: "Suggested At" }
      ]
    };
  },
  async mounted() {
    try {
      const response = await api.get("/user/history/", {
        withCredentials: true,
      });
      this.history = response.data;
    } catch (error) {
      console.error("Error loading history:", error);
    } finally {
      this.loading = false;
    }
  },
};
</script>
