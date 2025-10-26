import api from "@/api/base";
import { StaticInformationCreateInDto, StaticInformationListParamsType, StaticInformationUpdateInDto } from "@/types/api/static_information";

export const listStatisticInformation = async (filters: StaticInformationListParamsType={}) => {
    filters["admin"] = true
    return await api.get("static_information/",
        {
            params: filters
        },
    )
}

export const createStatisticInformation = async (createData: StaticInformationCreateInDto) => {
    return await api.post("static_information/", createData);
}

export const updateStatisticInformation = async (recordId: number, updateData: StaticInformationUpdateInDto) => {
    return await api.patch(`static_information/${recordId}/`, updateData);
}

export const deleteStatisticInformation = async (recordId: number) => {
    return await api.delete(`static_information/${recordId}/`);
}