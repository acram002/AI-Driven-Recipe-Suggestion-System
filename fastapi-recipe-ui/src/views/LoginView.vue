
<template>
  <b-container class="mt-5">
    <b-row class="justify-content-center">
      <b-col cols="6">
        <b-card title="Login" class="shadow">
          <b-form @submit.prevent="login">
            <b-form-group label="Email:" label-for="email">
              <b-form-input id="email" type="email" v-model="email" required></b-form-input>
            </b-form-group>

            <b-form-group label="Password:" label-for="password">
              <b-form-input id="password" type="password" v-model="password" required></b-form-input>
            </b-form-group>

            <b-button type="submit" variant="success" block>Login</b-button>
          </b-form>

          <b-alert v-if="errorMessage" variant="danger" show class="mt-3">
            {{ errorMessage }}
          </b-alert>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { BForm, BFormInput, BFormGroup, BButton, BAlert, BCard, BContainer, BRow, BCol } from 'bootstrap-vue-next';

const router = useRouter();
const auth = useAuthStore();

const email = ref("");
const password = ref("");
const errorMessage = ref("");

const login = async () => {
  try {
    await auth.login(email.value, password.value);
    router.push("/profile"); // Redirect after login
  } catch (error) {
    errorMessage.value = error.message;
  }
};
</script>


