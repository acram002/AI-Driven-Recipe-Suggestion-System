<template>

  <div id="app" class="d-flex flex-column min-vh-100">

    <!-- Navbar -->
    <Navbar />

    <!-- Page Content -->
    <main class="flex-grow-1">
      <router-view />
    </main>

    <!-- Footer -->
    <Footer />

  </div>

</template>

<script setup>
// ✅ Import Navbar and Footer from components
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
/* Background for full app */
body {
  background: linear-gradient(to right, #f0f4f8, #d9e2ec, #bcccdc);
  font-family: 'Poppins', 'Roboto', sans-serif;
  color: #2f3e46;
  min-height: 100vh;
  margin: 0;
}

/* Main container should grow and push footer to bottom */
main {
  padding: 20px;
}

/* Button style */
button, .b-button {
  border-radius: 25px;
  transition: all 0.3s ease;
}

.b-button:hover {
  transform: scale(1.05);
}

/* Card style */
.card, .b-card {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-radius: 12px;
  background: white;
  padding: 20px;
  animation: fadeInUp 0.6s ease forwards;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Animations */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
