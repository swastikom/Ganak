import axios from "axios";

function isServer() {
    return typeof window === "undefined";
}

const axiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "https://ganak-xwdx.onrender.com/",
});

const getAxiosInstance = (isClient: any) => {
    if (isClient) {
        axiosInstance.interceptors.request.use(
            (config) => {
                const token = localStorage.getItem("authToken");
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );

        axiosInstance.interceptors.response.use(
            (response) => {
                return response;
            },
            (error) => {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem("authToken");
                    localStorage.removeItem("user");
                }
                return Promise.reject(error);
            }
        );
    }

    return axiosInstance;
};

export default getAxiosInstance;
