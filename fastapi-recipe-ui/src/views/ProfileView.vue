<template>
  <b-container class="mt-5">
    <b-row class="justify-content-center">
<<<<<<< HEAD
      <b-col cols="6">
        <b-card title="Profile" class="shadow">
          <b-card-text v-if="user">
            <p><strong>Name:</strong> {{ user.name }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
          </b-card-text>
          <b-alert v-else variant="info" show>Loading...</b-alert>
=======
      <b-col cols="12" md="8" lg="6">
        <b-card class="shadow-lg p-4 profile-card">

          <div class="text-center mb-4">
            <h3><strong>👤 My Profile</strong></h3>
          </div>

          <div v-if="user" class="profile-info">

            <div class="info-row">
              <span class="info-label">👤 Name:</span>
              <span class="info-value">{{ user.name }}</span>
            </div>

            <div class="info-row">
              <span class="info-label">📧 Email:</span>
              <span class="info-value">{{ user.email }}</span>
            </div>

            <!-- Optionally in future: add more details like phone, location, bio -->

          </div>

          <b-alert v-else variant="info" show class="text-center mt-4">
            Loading user data...
          </b-alert>

>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
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
<<<<<<< HEAD

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
=======
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

<style scoped>
.profile-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
}

/* Profile Heading */
h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #343a40;
}

/* Profile Info Layout */
.profile-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  background: #f8f9fa;
  font-size: 1.1rem;
}

.info-label {
  font-weight: bold;
  color: #495057;
}

.info-value {
  color: #495057;
}

/* Alert */
.b-alert {
  font-size: 1.1rem;
}
</style>
>>>>>>> 4c75fa8 (Initial commit with liked-recipes feature)
