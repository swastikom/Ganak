import axios from 'axios';

interface LoginPayload {
    username: string;
    password: string;
}

export const login = async (payload: LoginPayload): Promise<any> => {
    const formData = new URLSearchParams();
    formData.append('username', payload.username);
    formData.append('password', payload.password);

    try {
        const response = await axios.post(
            'https://ganak-xwdx.onrender.com/token',
            formData,
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }
        );
        return response.data;
    } catch (error: any) {
        if (error.response) {
            console.error('Login error response data:', error.response.data);
            console.error('Login error response status:', error.response.status);
            console.error('Login error response headers:', error.response.headers);
        }
        throw error;
    }
};
