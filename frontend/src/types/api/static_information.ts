import type {TableDataItemType} from "../ui/table";
import type { ColumnType } from 'antd/es/table'


export type StaticInformationAvailableAsType = "string" | "number" | "float" | "boolean" | "json" | "date" | "time" | "datetime"

export type StaticInformationCreateInDto = {
    name: string
    title: string
    value: string
    as_type: StaticInformationAvailableAsType
}

export type StaticInformationUpdateInDto = {
    name?: string
    title?: string
    value?: string
    as_type?: StaticInformationAvailableAsType
}

export type StaticInformationListParamsType = {
    admin?: boolean,
    as_type?: StaticInformationAvailableAsType[]
    name?: string
    title?: string
}

export type StaticInformationOutDto = {
    id: number
    name: string
    title: string
    value: string
    as_type: StaticInformationAvailableAsType
}

export type StaticInformationListOutDto = StaticInformationOutDto[]


export type StaticInformationTableDataItemType = StaticInformationOutDto & TableDataItemType

export type GetStaticInformationTableColumnsType = (
    filters: StaticInformationListParamsType,
    setFilters: (filtersData: StaticInformationListParamsType) => void,
) => ColumnType<StaticInformationTableDataItemType>[]