import type {AxiosResponse} from "axios";
import api from "@/api/base";
import {loginCredentialsType} from "@/types/api/login";
import {LoginResponseType} from "@/types/api/auth";

const authApiLogin = async (
    credentials: loginCredentialsType
): Promise<LoginResponseType> => {
    const response: AxiosResponse<LoginResponseType> = await api.post<LoginResponseType>(
        "auth/token/",
        {
            username: credentials.username,
            password: credentials.password
        },
        { withCredentials: true }
    );
    return response.data;
};

export default authApiLogin;