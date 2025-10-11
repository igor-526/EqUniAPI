import api from "./baseApi.ts";
import type { LoginResponseType } from "../types/authTypes.ts";
import type {AxiosResponse} from "axios";

const authApiLogin = async (
    login: string,
    password: string
): Promise<LoginResponseType> => {
    const response: AxiosResponse<LoginResponseType> = await api.post<LoginResponseType>(
        "auth/token/",
        {
            username: login,
            password: password
        },
        { withCredentials: true }
    );
    return response.data;
};

export default authApiLogin;