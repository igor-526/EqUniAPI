import api from "./baseApi.ts";

export const getBreedList = async (filters={}) => {
    return await api.get("horses/breeds",
        {
            params: filters
        },
    )
}