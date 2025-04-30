<template>

  <b-container class="mt-5">

    <b-row class="justify-content-center">

      <b-col cols="6">

        <b-card title="Dietary Preferences" class="shadow">

          <b-form v-if="preferences">

            <b-form-group label="Dietary Preferences:" label-for="dietary_preferences">
              <b-form-input id="dietary_preferences" v-model="preferences.dietary_preferences"></b-form-input>
            </b-form-group>

            <b-form-group label="Allergies:" label-for="allergies">
              <b-form-input id="allergies" v-model="preferences.allergies"></b-form-input>
            </b-form-group>

            <b-form-group label="Disliked Ingredients:" label-for="disliked_ingredients">
              <b-form-input id="disliked_ingredients" v-model="preferences.disliked_ingredients"></b-form-input>
            </b-form-group>

            <b-button @click="updatePreferences" variant="success" block>Save</b-button>
            
          </b-form>

          <b-alert v-else variant="info" show>Loading...</b-alert>

        </b-card>

        <div v-if="popupMessage" class="popup-alert" :class="popupType">
          {{ popupMessage }}
        </div>

      </b-col>

    </b-row>

  </b-container>

</template>



<script setup>
import { ref, onMounted } from "vue";
import api from "@/api";
import { BForm, BFormInput, BFormGroup, BButton, BAlert, BCard, BContainer, BRow, BCol } from 'bootstrap-vue-next';

const preferences = ref(null);
const message = ref("");

const popupMessage = ref('')
const popupType = ref('') // 'success' or 'error'

const showPopup = (message, type = 'success') => {
  popupMessage.value = message
  popupType.value = type

  setTimeout(() => {
    popupMessage.value = ''
    popupType.value = ''
  }, 3000)
}

onMounted(async () => {

  try {

    const response = await api.get("/user/preferences/", { withCredentials: true });
    
    preferences.value = response.data;

  } catch (error) {

    console.error("Error fetching preferences", error);
    
  }

});


const updatePreferences = async () => {
  
  try {

    const response = await api.put(
      "/user/preferences/",
      preferences.value,
      { withCredentials: true }
    );

    message.value = response.data.message;
    showPopup(message || 'Recipe liked! 👍', 'success')


  } catch (error) {

    message.value = "Failed to update preferences.";
    showPopup(error.response?.data?.detail || 'Error liking recipe', 'error')

  }

};

</script>

<style scoped>

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

</style>