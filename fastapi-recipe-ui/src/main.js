import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

// Import styles
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css';

const app = createApp(App);

app.use(createPinia());
app.use(router);

// Dynamically import BootstrapVueNext
import('bootstrap-vue-next').then(({ BootstrapVueNext }) => {
  app.use(BootstrapVueNext)
  app.mount('#app')
})
