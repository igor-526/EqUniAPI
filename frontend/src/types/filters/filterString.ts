import type {FiltersBaseType} from "./filterBase.ts";
import type {ReactNode} from "react";

type FilterStringPropsType = {
    filters: FiltersBaseType
    setFilters: (filters: FiltersBaseType) => void,
    filterKey: string,
    placeHolder?: string,
}

export type GetFilterStringElementType = (props: FilterStringPropsType) => ReactNode