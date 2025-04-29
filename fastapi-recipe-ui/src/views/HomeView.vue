<template>
<<<<<<< HEAD

  <b-container class="mt-5">

    <b-row>

      <b-col cols="12" md="8" class="mx-auto">

        <b-form @submit.prevent="getSuggestions">

          <b-input-group>

            <b-form-input
              v-model="ingredientInput"
              placeholder="Enter ingredients..."
            ></b-form-input>
            <template #append>
              <b-button variant="danger" @click="clearInput">×</b-button>
            </template>

          </b-input-group>

          <div class="d-flex justify-content-end mt-2">
            <b-button type="submit" variant="primary" class="me-2">Get Suggestions</b-button>
            <b-button variant="secondary" @click="clearResults">Clear Results</b-button>
          </div>

        </b-form>

        <div v-if="results.length" class="mt-5">

=======
  <b-container class="mt-5">
    <b-form @submit.prevent="getSuggestions">
      <b-input-group class="search-box">
        <b-form-input
          v-model="ingredientInput"
          placeholder="Enter ingredients like Tomato, Pasta..."
          class="form-control-lg"
        ></b-form-input>
        <template #append>
          <b-button variant="danger" @click="clearInput" class="rounded-right">×</b-button>
        </template>
      </b-input-group>

      <div class="d-flex justify-content-center mt-4 button-group">
        <b-button type="submit" variant="primary" class="search-btn">🔍 Get Suggestions</b-button>
        <b-button variant="outline-secondary" class="clear-btn ml-3" @click="clearResults">🧹 Clear</b-button>
      </div>
    </b-form>

    <!-- Suggestions Results -->
    <div v-if="results.length" class="mt-5">
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
      <h4 class="mb-3">Recipe Suggestions</h4>

      <b-card
        v-for="(recipe, index) in results"
<<<<<<< HEAD
        :key="index"
=======
        :key="recipe.suggestion_id"
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
        class="mb-3"
        bg-variant="light"
        border-variant="primary"
      >
        <h5>{{ recipe.title }}</h5>
        <p>{{ recipe.description }}</p>

<<<<<<< HEAD
      </b-card>

    </div>

      </b-col>

    </b-row>

  </b-container>

=======
        <!-- Like/Dislike buttons -->
        <div class="d-flex justify-content-start gap-3 mt-3">
          <b-button variant="success" size="sm" @click="likeRecipe(index)">
            👍 Like
          </b-button>
          <b-button variant="danger" size="sm" @click="dislikeRecipe(index)">
            👎 Dislike
          </b-button>
        </div>

      </b-card>
    </div>
  </b-container>
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
</template>

<script setup>
import {
  BContainer,
<<<<<<< HEAD
  BRow,
  BCol,
=======
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
  BForm,
  BFormInput,
  BInputGroup,
  BButton,
  BCard
} from 'bootstrap-vue-next'

import { ref } from 'vue'
import api from '@/api'

const ingredientInput = ref('')
const results = ref([])

<<<<<<< HEAD
=======
// Fetch recipe suggestions
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
const getSuggestions = async () => {
  try {
    const response = await api.post('/suggest/', { ingredients: ingredientInput.value })
    results.value = response.data.recipes
  } catch (error) {
    console.error('API error:', error)
  }
}

<<<<<<< HEAD
=======
// Clear input field
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
const clearInput = () => {
  ingredientInput.value = ''
}

<<<<<<< HEAD
=======
// Clear all suggestions
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
const clearResults = () => {
  results.value = []
}

<<<<<<< HEAD
</script>
=======
// Like a recipe
const likeRecipe = async (index) => {
  try {
    const suggestionId = results.value[index].suggestion_id
    await api.post('/suggestion/feedback/', {
      suggestion_id: suggestionId,
      liked: true
    })
    console.log('Liked recipe:', results.value[index].title)
  } catch (error) {
    console.error('Like error:', error)
  }
}

// Dislike a recipe
const dislikeRecipe = async (index) => {
  try {
    const suggestionId = results.value[index].suggestion_id
    await api.post('/suggestion/feedback/', {
      suggestion_id: suggestionId,
      liked: false
    })
    console.log('Disliked recipe:', results.value[index].title)
  } catch (error) {
    console.error('Dislike error:', error)
  }
}
</script>

<style scoped>
/* Enlarge and beautify search box */
.search-box {
  max-width: 700px;
  margin: 0 auto;
  margin-bottom: 20px;
}

.b-form-input, .form-control-lg {
  height: 55px;
  font-size: 1.2rem;
  padding: 10px 20px;
  border-radius: 30px 0 0 30px;
  border: 2px solid #74c0fc;
}

/* Buttons */
.search-btn {
  padding: 10px 25px;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 600;
}

.clear-btn {
  padding: 10px 25px;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 600;
}

.b-button {
  border-radius: 30px;
}

/* Recipe cards */
.b-card {
  animation: fadeInUp 0.5s ease forwards;
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
