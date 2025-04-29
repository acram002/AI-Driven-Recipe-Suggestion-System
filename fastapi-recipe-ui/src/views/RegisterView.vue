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

        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

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
  }
};
</script>

<style scoped>
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
}
</style>
