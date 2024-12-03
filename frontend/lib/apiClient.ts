import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios';

// Create an instance of axios
const apiClient: AxiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/v1',  
    timeout: 10000,  
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request/response interceptors for handling tokens, etc.
apiClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
        // Modify the request config before the request is sent
        // For example, add a token if needed:
        // const token = localStorage.getItem('token');
        // if (token) config.headers.Authorization = `Bearer ${token}`;
        return config;
    },
    (error: any) => {
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
        // Handle responses globally
        console.log('API Response:', response);
        return response.data;
    },
    (error: any) => {
        // Handle errors globally
        console.error('API Error:', error);
        return Promise.reject(error.response?.data || error.message);
    }
);

export default apiClient;
