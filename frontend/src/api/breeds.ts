import api from "@/api/base";
import {HorseBreedsAPIFiltersType} from "@/types/api/horseBreed";

export const getBreedList = async (filters: HorseBreedsAPIFiltersType={}) => {
    return await api.get("horses/breeds",
        {
            params: filters
        },
    )
}