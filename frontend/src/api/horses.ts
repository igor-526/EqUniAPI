import api from "@/api/base";
import {HorseAPIFiltersType} from "@/types/api/horse";

export const getHorsesList = async (filters: HorseAPIFiltersType={}) => {
    filters["pedigree"] = 1
    return await api.get("horses/",
        {
            params: filters
        },
    )
}