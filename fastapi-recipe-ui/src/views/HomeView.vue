<template>

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

      <h4 class="mb-3">Recipe Suggestions</h4>

      <b-card
        v-for="(recipe, index) in results"
        :key="index"
        class="mb-3"
        bg-variant="light"
        border-variant="primary"
      >
        <h5>{{ recipe.title }}</h5>
        <p>{{ recipe.description }}</p>

      </b-card>

    </div>

      </b-col>

    </b-row>

  </b-container>

</template>

<script setup>
import {
  BContainer,
  BRow,
  BCol,
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

const getSuggestions = async () => {
  try {
    const response = await api.post('/suggest/', { ingredients: ingredientInput.value })
    results.value = response.data.recipes
  } catch (error) {
    console.error('API error:', error)
  }
}

const clearInput = () => {
  ingredientInput.value = ''
}

const clearResults = () => {
  results.value = []
}

</script>
