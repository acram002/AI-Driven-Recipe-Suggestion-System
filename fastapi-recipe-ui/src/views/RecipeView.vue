<template>
  <div class="recipe-view">
    <h2>AI Recipe Generator</h2>

    <input v-model="ingredientsText" placeholder="Enter ingredients (e.g., chicken, tomato)" />
    <button @click="getRecipe">Generate Recipe</button>

    <div v-if="recipe">
      <h3>Recipe:</h3>
      <pre>{{ recipe }}</pre>

      <label for="rating">Rate this recipe:</label>
      <select v-model="rating">
        <option value="5">⭐️⭐️⭐️⭐️⭐️</option>
        <option value="4">⭐️⭐️⭐️⭐️</option>
        <option value="3">⭐️⭐️⭐️</option>
        <option value="2">⭐️⭐️</option>
        <option value="1">⭐️</option>
      </select>
      <button @click="sendFeedback">Submit Feedback</button>
    </div>
  </div>
</template>

<script>
import { generateRecipe, submitFeedback } from '@/api/index.js';

export default {
  data() {
    return {
      ingredientsText: '',
      recipe: '',
      rating: 5,
    };
  },
  methods: {
    async getRecipe() {
      const ingredients = this.ingredientsText.split(',').map(i => i.trim());
      const response = await generateRecipe(ingredients);
      this.recipe = response.recipe;
    },
    async sendFeedback() {
      if (!this.recipe) {
        alert("Please generate a recipe first.");
        return;
      }
      await submitFeedback(this.recipe, this.rating);
      alert("Thanks for your feedback!");
    },
  },
};
</script>

<style scoped>
.recipe-view {
  padding: 1.5rem;
}
</style>
