import axios, {type AxiosInstance, type AxiosResponse, type AxiosRequestConfig } from 'axios';

interface CustomAxiosInstance extends AxiosInstance {
    post<T = any, R = AxiosResponse<T>, D = any>(
        url: string,
        data?: D,
        config?: AxiosRequestConfig<D>
    ): Promise<R>;
}

const backendUrl: string = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : "http://localhost:8009/api/v1"

const api: CustomAxiosInstance = axios.create({
    baseURL: backendUrl,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true
}) as CustomAxiosInstance;

let isRefreshing = false;

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry &&
            !originalRequest.url.includes('/auth/token/refresh/')) {

            if (isRefreshing) {
                return Promise.reject(error);
            }

            originalRequest._retry = true;
            isRefreshing = true;

            try {
                const response = await api.post('/auth/token/refresh/', {}, { withCredentials: true });

                localStorage.setItem('accessToken', response.data.access);
                originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
                isRefreshing = false;

                return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('accessToken');
                isRefreshing = false;

                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }

                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;