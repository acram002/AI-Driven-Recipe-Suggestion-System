<<<<<<< HEAD
<script setup>
import { BForm, BFormInput, BFormGroup, BButton, BAlert, BCard, BContainer, BRow, BCol } from 'bootstrap-vue-next';
</script>

<template>
  <b-container class="mt-5">
    <b-row class="justify-content-center">
      <b-col cols="6">
        <b-card title="User Registration" class="shadow">
          <b-form @submit.prevent="registerUser">
            <b-form-group label="Name:" label-for="name">
              <b-form-input id="name" v-model="formData.name" required></b-form-input>
            </b-form-group>

            <b-form-group label="Email:" label-for="email">
              <b-form-input id="email" type="email" v-model="formData.email" required></b-form-input>
            </b-form-group>

            <b-form-group label="Password:" label-for="password">
              <b-form-input id="password" type="password" v-model="formData.password" required></b-form-input>
            </b-form-group>

            <b-button type="submit" variant="primary" block>Register</b-button>
          </b-form>

          <b-alert v-if="message" :variant="isSuccess ? 'success' : 'danger'" show class="mt-3">
            {{ message }}
          </b-alert>
=======
<template>
  <b-container class="mt-5">
    <b-row class="justify-content-center">
      <b-col cols="12" md="6" lg="5">
        <b-card class="shadow-lg p-4 register-card">

          <h3 class="text-center mb-4"><strong>📝 Create Account</strong></h3>

          <b-form @submit.prevent="registerUser">

            <b-form-group 
              label="Full Name" 
              label-for="name" 
              label-class="font-weight-bold"
            >
              <b-form-input 
                id="name" 
                v-model="formData.name" 
                required 
                placeholder="Enter your full name"
              ></b-form-input>
            </b-form-group>

            <b-form-group 
              label="Email Address" 
              label-for="email" 
              label-class="font-weight-bold"
            >
              <b-form-input 
                id="email" 
                type="email" 
                v-model="formData.email" 
                required 
                placeholder="Enter your email"
              ></b-form-input>
            </b-form-group>

            <b-form-group 
              label="Password" 
              label-for="password" 
              label-class="font-weight-bold"
            >
              <b-form-input 
                id="password" 
                type="password" 
                v-model="formData.password" 
                required 
                placeholder="Create a strong password"
              ></b-form-input>
            </b-form-group>

            <div class="text-center mt-4">
              <b-button type="submit" variant="primary" class="register-btn">
                🚀 Register
              </b-button>
            </div>

          </b-form>

          <div class="text-center mt-4">
            <p class="bold-text">Already have an account?</p>
            <b-button variant="outline-primary" size="sm" class="login-btn" @click="router.push('/login')">
              🔑 Login Here
            </b-button>
          </div>

          <b-alert v-if="message" :variant="isSuccess ? 'success' : 'danger'" show class="mt-3 text-center">
            {{ message }}
          </b-alert>

>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<<<<<<< HEAD

<script>
import api from '@/api';
import { BForm, BFormInput, BFormGroup, BButton, BAlert, BCard, BContainer, BRow, BCol } from 'bootstrap-vue-next';

export default {
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: ''
      },
      message: '',
      isSuccess: false
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await api.post('/register/', this.formData);
        this.message = response.data.message;
        this.isSuccess = true;

        // Redirect to login page after 2 seconds
          setTimeout(() => {
            router.push('/login');
          }, 2000);
          
      } catch (error) {
        this.message = error.response?.data?.detail || 'Registration failed!';
        this.isSuccess = false;
      }
    }
=======
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from '@/api';
import { BForm, BFormInput, BFormGroup, BButton, BAlert, BCard, BContainer, BRow, BCol } from 'bootstrap-vue-next';

const router = useRouter();

const formData = ref({
  name: '',
  email: '',
  password: ''
});

const message = ref('');
const isSuccess = ref(false);

const registerUser = async () => {
  try {
    const response = await api.post('/register/', formData.value);
    message.value = response.data.message;
    isSuccess.value = true;

    // Redirect to login page after 2 seconds
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error) {
    message.value = error.response?.data?.detail || 'Registration failed!';
    isSuccess.value = false;
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
  }
};
</script>

<style scoped>
<<<<<<< HEAD
.register-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
}
input {
  width: 100%;
  padding: 8px;
  margin: 8px 0;
}
button {
  background-color: blue;
  color: white;
  padding: 10px;
  border: none;
  width: 100%;
}
.success {
  color: green;
}
.error {
  color: red;
=======
.register-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
}

/* Big nice Register button */
.register-btn {
  border-radius: 30px;
  font-size: 1.2rem;
  padding: 12px 30px;
  font-weight: bold;
}

/* Login button under register */
.login-btn {
  margin-top: 10px;
  padding: 8px 20px;
  border-radius: 25px;
}

/* Bold text */
.bold-text {
  font-weight: bold;
  font-size: 1rem;
}

/* Input styling */
.b-form-input {
  border-radius: 20px;
  padding: 12px 20px;
  font-size: 1rem;
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
}
</style>
