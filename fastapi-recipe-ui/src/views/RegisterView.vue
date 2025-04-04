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
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>


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
  }
};
</script>

<style scoped>
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
}
</style>
