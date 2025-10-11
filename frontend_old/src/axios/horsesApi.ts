import api from "./baseApi.ts";

export const getHorsesList = async (filters={}) => {
    filters["pedigree"] = 1
    return await api.get("horses/",
        {
            params: filters
        },
    )
}