import axios, {type AxiosInstance, type AxiosResponse, type AxiosRequestConfig } from 'axios';

interface CustomAxiosInstance extends AxiosInstance {
    post<T = any, R = AxiosResponse<T>, D = any>(
        url: string,
        data?: D,
        config?: AxiosRequestConfig<D>
    ): Promise<R>;
}

const backendUrl: string = "http://localhost:8000/api/v1"

const api: CustomAxiosInstance = axios.create({
    baseURL: backendUrl,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true
}) as CustomAxiosInstance;

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 &&
            !originalRequest.url.includes('/auth/token/')) {
        }
        return Promise.reject(error);
    }
);

export default api;