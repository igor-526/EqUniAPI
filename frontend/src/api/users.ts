import api from "@/api/base";
import {UserListRequestParamsType, UserRegistrationInDtoType} from "@/types/api/users";

export const getUsersPageMetadata = async () => {
    return await api.get("users/page_metadata")
}

export const getUsersList = async (filters: UserListRequestParamsType={}) => {
    return await api.get("users/",
        {
            params: filters
        },
    )
}

export const registerUser = async (userData: UserRegistrationInDtoType) => {
    return await api.post("users/", userData);
}
