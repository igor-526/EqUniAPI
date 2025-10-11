import type {ReactNode} from "react";
import type {FiltersBaseType} from "./filterBaseTypes.ts";

export type FilterListDataType = {
    label: string,
    value: string | number,
    key: string
}

type FilterListPropsType = {
    filters: FiltersBaseType
    setFilters: (filters: FiltersBaseType) => void,
    filterKey: string,
    filterData: FilterListDataType[],
    placeHolder: string,
}

export type GetFilterListElementType = (props: FilterListPropsType) => ReactNode