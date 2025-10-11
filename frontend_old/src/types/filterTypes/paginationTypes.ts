import type {FiltersBaseType} from "./filterBaseTypes.ts";
import type {ReactNode} from "react";

type TablePaginationPropsType = {
    setFilters: (filters: FiltersBaseType) => void,
    total: number
}

export type GetTablePaginationElementType = (props: TablePaginationPropsType) => ReactNode