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
          <b-alert v-if="message" variant="success" show class="mt-3">{{ message }}</b-alert>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>



<script setup>
import { ref, onMounted } from "vue";
import api from "@/api";
import { useRouter } from "vue-router";
import { BForm, BFormInput, BFormGroup, BButton, BAlert, BCard, BContainer, BRow, BCol } from 'bootstrap-vue-next';

const preferences = ref(null);
const message = ref("");
const router = useRouter();

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

  } catch (error) {

    console.error("Error updating preferences", error);
    message.value = "Failed to update preferences.";

  }

};

</script>
