<<<<<<< HEAD

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
=======
<template>
  <b-container class="mt-5">
    <b-row class="justify-content-center">
      <b-col cols="12" md="6" lg="5">
        <b-card class="shadow-lg p-4 login-card">

          <h3 class="text-center mb-4">🔑 <strong>Welcome Back</strong></h3>

          <b-form @submit.prevent="login">

            <b-form-group 
              label="Email Address" 
              label-for="email" 
              label-cols-sm="12" 
              label-align-sm="left" 
              label-class="font-weight-bold"
            >
              <b-form-input 
                id="email" 
                type="email" 
                v-model="email" 
                required 
                placeholder="Enter your email"
              ></b-form-input>
            </b-form-group>

            <b-form-group 
              label="Password" 
              label-for="password" 
              label-cols-sm="12" 
              label-align-sm="left" 
              label-class="font-weight-bold"
            >
              <b-form-input 
                id="password" 
                type="password" 
                v-model="password" 
                required 
                placeholder="Enter your password"
              ></b-form-input>
            </b-form-group>

            <div class="text-center mt-4">
              <b-button type="submit" variant="primary" class="login-btn">
                🔓 Login
              </b-button>
            </div>

          </b-form>

          <div class="text-center mt-4">
            <p class="bold-text">Don't have an account?</p>
            <b-button variant="outline-success" size="sm" class="register-btn" @click="router.push('/register')">
              📝 Register Here
            </b-button>
          </div>

          <b-alert v-if="errorMessage" variant="danger" show class="mt-3 text-center">
            {{ errorMessage }}
          </b-alert>

>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
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
<<<<<<< HEAD
    errorMessage.value = error.message;
=======
    errorMessage.value = error.message || "Login failed!";
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
  }
};
</script>

<<<<<<< HEAD

=======
<style scoped>
.login-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
}

/* Center Login button */
.login-btn {
  border-radius: 30px;
  font-size: 1.2rem;
  padding: 12px 30px;
  font-weight: bold;
}

/* Register button */
.register-btn {
  margin-top: 10px;
  padding: 8px 20px;
  border-radius: 25px;
}

/* Bold "Don't have account" text */
.bold-text {
  font-weight: bold;
  font-size: 1rem;
}

/* Inputs */
.b-form-input {
  border-radius: 20px;
  padding: 12px 20px;
  font-size: 1rem;
}
</style>
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
