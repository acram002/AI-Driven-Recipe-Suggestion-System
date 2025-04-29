import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // FastAPI backend URL
    withCredentials: true, // Ensure cookies are sent
});

// Manually ensure cookies are attached (for stubborn browsers)
api.interceptors.request.use((config) => {
    config.withCredentials = true;
    console.log('Cookies being sent:', document.cookie);

    return config;
});

export default api;
