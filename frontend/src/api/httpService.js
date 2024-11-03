import axios from 'axios';

// Create an instance of axios
const httpService = axios.create({
    baseURL: 'http://localhost:8000/api/v1',  
    timeout: 10000,  
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request/response interceptors for handling tokens, etc.
httpService.interceptors.request.use(
    (config) => {
        // Modify the request config before the request is sent
        // For example, add a token if needed:
        // const token = localStorage.getItem('token');
        // if (token) config.headers.Authorization = `Bearer ${token}`;
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

httpService.interceptors.response.use(
    (response) => {
        // Handle responses globally
        console.log('API Response:', response);
        return response.data;
    },
    (error) => {
        // Handle errors globally
        console.error('API Error:', error);
        return Promise.reject(error.response.data || error.message);
    }
);

export default httpService;
