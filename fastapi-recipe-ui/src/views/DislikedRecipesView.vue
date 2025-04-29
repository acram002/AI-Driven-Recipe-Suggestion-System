<template>
  <b-container class="mt-5">
    <h3 class="mb-4">👎 Disliked Recipes</h3>

    <div v-if="loading" class="text-center">
      <b-spinner label="Loading..."></b-spinner>
    </div>

    <div v-else>
      <b-card
        v-for="(recipe, index) in dislikedRecipes"
        :key="recipe.suggestion_id"
        class="mb-3"
        bg-variant="light"
        border-variant="danger"
      >
        <h5>{{ recipe.title }}</h5>
        <p>{{ recipe.description }}</p>

        <div class="d-flex justify-content-end">
          <b-button variant="success" size="sm" @click="likeRecipe(index)">
            👍 Like Again
          </b-button>
        </div>
      </b-card>

      <div v-if="dislikedRecipes.length === 0" class="text-center mt-5">
        <p>No disliked recipes found. Excellent taste! 🎉</p>
      </div>
    </div>

    <!-- Go Back Button -->
    <div class="d-flex justify-content-center mt-5">
      <b-button variant="outline-primary" class="back-btn" @click="goToLiked">
        ❤️ View Liked Recipes
      </b-button>
    </div>
  </b-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { BContainer, BCard, BButton, BSpinner } from 'bootstrap-vue-next'

const dislikedRecipes = ref([])
const loading = ref(true)
const router = useRouter()

onMounted(async () => {
  await fetchDislikedRecipes()
})

const fetchDislikedRecipes = async () => {
  try {
    const response = await api.get('/user/disliked_recipes/')
    dislikedRecipes.value = response.data
  } catch (error) {
    console.error('Error fetching disliked recipes:', error)
  } finally {
    loading.value = false
  }
}

const likeRecipe = async (index) => {
  try {
    const suggestionId = dislikedRecipes.value[index].suggestion_id
    await api.post('/suggestion/feedback/', {
      suggestion_id: suggestionId,
      liked: true
    })
    dislikedRecipes.value.splice(index, 1)
  } catch (error) {
    console.error('Error liking recipe again:', error)
  }
}

const goToLiked = () => {
  router.push('/liked')
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

.back-btn {
  padding: 10px 25px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #74c0fc;
  color: white;
}
</style>
