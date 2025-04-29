<template>
  <b-container class="mt-5">
    <h3 class="mb-4">❤️ Liked Recipes</h3>

    <b-card
      v-for="(recipe, index) in likedRecipes"
      :key="recipe.suggestion_id"
      class="mb-3"
      bg-variant="light"
      border-variant="success"
    >
      <h5>{{ recipe.title }}</h5>
      <p>{{ recipe.description }}</p>

      <div class="d-flex justify-content-end">
        <b-button variant="danger" size="sm" @click="dislikeRecipe(index)">
          👎 Dislike
        </b-button>
      </div>
    </b-card>

    <div v-if="likedRecipes.length === 0" class="text-center mt-5">
      <p>No liked recipes found yet. Start exploring! 🚀</p>
    </div>

    <!-- 🚀 Disliked Recipes Button -->
    <div class="d-flex justify-content-center mt-5">
      <b-button variant="outline-danger" class="disliked-btn" @click="goToDisliked">
        👎 View Disliked Recipes
      </b-button>
    </div>
  </b-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'
import { BContainer, BCard, BButton } from 'bootstrap-vue-next'

const likedRecipes = ref([])
const router = useRouter()

// Fetch liked recipes
onMounted(async () => {
  await fetchLikedRecipes()
})

const fetchLikedRecipes = async () => {
  try {
    const response = await api.get('/user/liked_recipes/')
    likedRecipes.value = response.data
  } catch (error) {
    console.error('Error fetching liked recipes:', error)
  }
}

// Dislike recipe from list
const dislikeRecipe = async (index) => {
  try {
    const suggestionId = likedRecipes.value[index].suggestion_id
    await api.post('/suggestion/feedback/', {
      suggestion_id: suggestionId,
      liked: false
    })
    likedRecipes.value.splice(index, 1)
  } catch (error) {
    console.error('Error disliking recipe:', error)
  }
}

// 🚀 Navigate to Disliked Recipes page
const goToDisliked = () => {
  router.push('/disliked')
}
</script>

<style scoped>
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

/* Disliked Button Styling */
.disliked-btn {
  padding: 10px 25px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.disliked-btn:hover {
  background-color: #ff6b6b;
  color: white;
}
</style>
