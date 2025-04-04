<template>
  <b-container class="mt-5">
    <b-row class="justify-content-center">
      <b-col cols="6">
        <b-card title="Profile" class="shadow">
          <b-card-text v-if="user">
            <p><strong>Name:</strong> {{ user.name }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
          </b-card-text>
          <b-alert v-else variant="info" show>Loading...</b-alert>
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

const user = ref(null);
const router = useRouter();

onMounted(async () => {

try {

    const response = await api.get("/user/profile/", { withCredentials: true });
    user.value = response.data;

  } catch (error) {

    if (error.response && error.response.status === 401) {
      router.push("/login");
    }

  }

});


</script>
