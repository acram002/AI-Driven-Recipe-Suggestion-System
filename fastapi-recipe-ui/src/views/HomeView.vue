<template>

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

      <h4 class="mb-3">Recipe Suggestions</h4>

      <b-card
        v-for="(recipe, index) in results"
        :key="recipe.recipe_id"
        class="mb-3"
        bg-variant="light"
        border-variant="primary"
      >
        <h5>{{ recipe.title }}</h5>
        <p>{{ recipe.description }}</p>

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

    <div v-if="popupMessage" class="popup-alert" :class="popupType">
      {{ popupMessage }}
    </div>

    <div v-if="loading" class="popup-alert loading">Loading...</div>

  </b-container>

</template>

<script setup>
import {
  BContainer,
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

const popupMessage = ref('')
const popupType = ref('') // 'success' or 'error'

const loading = ref(false)

const showPopup = (message, type = 'success') => {
  popupMessage.value = message
  popupType.value = type

  setTimeout(() => {
    popupMessage.value = ''
    popupType.value = ''
  }, 3000)
}

// Fetch recipe suggestions
const getSuggestions = async () => {

  try {

    loading.value = true
    const response= await api.post('/suggest/', { ingredients: ingredientInput.value })
    results.value = response.data.recipes

  } catch (error) {

    console.error('API error:', error)

  } finally {
    loading.value = false
  }

}

// Clear input field
const clearInput = () => {
  ingredientInput.value = ''
}

// Clear all suggestions
const clearResults = () => {
  results.value = []
}

// Like a recipe
const likeRecipe = async (index) => {
  try {
    const suggestionId = results.value[index].recipe_id
    const res = await api.post('/suggestion/feedback/', {
      suggestion_id: suggestionId,
      liked: true
    })

    showPopup(res.data.message || 'Recipe liked! 👍', 'success')

  } catch (error) {

    showPopup(error.response?.data?.detail || 'Error liking recipe', 'error')
    
  }
}

// Dislike a recipe
const dislikeRecipe = async (index) => {
  try {
    const suggestionId = results.value[index].recipe_id
    const res = await api.post('/suggestion/feedback/', {
      suggestion_id: suggestionId,
      liked: false
    })

    showPopup(res.data.message || 'Recipe disliked! 👎', 'success')

  } catch (error) {

    showPopup(error.response?.data?.detail || 'Error disliking recipe', 'error')

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

.popup-alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 25px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  z-index: 9999;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: opacity 0.3s ease;
}

.popup-alert.success {
  background-color: #28a745;
}

.popup-alert.error {
  background-color: #dc3545;
}

.popup-alert.loading {
  background-color: #527405;
}

</style>
