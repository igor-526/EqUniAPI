import {type ReactNode} from "react";
import { Dayjs } from 'dayjs';
import type {FiltersBaseType} from "./filterBaseTypes.ts";

type FilterDateRangePropsType = {
    setFilters: (filters: FiltersBaseType) => void,
    dateRange: any,
    setDateRange: (dr: DateRangeType | null) => void,
    filterKeyFrom: string,
    filterKeyTo: string,
}

export type GetFilterDateRangeElementType = (props: FilterDateRangePropsType) => ReactNode

export type DateRangeType = {
    0: Dayjs | null,
    1: Dayjs | null,
}