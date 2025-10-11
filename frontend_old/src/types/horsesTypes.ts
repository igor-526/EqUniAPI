import type {TableColumnType, TableDataItemType} from "./tableTypes";
import type {ApiListPaginatedResponseType} from "./apiTypes";
import type {HorseBreedsType} from "./horseBreedTypes";
import type {HorseOwnerType} from "./horseOwnerTypes";
import type {GalleryPhotoType} from "./galleryTypes";
import type { ColumnType } from 'antd/es/table'
import {FilterListDataType} from "./filterTypes/filterListTypes";


type HorseSexType = 0 | 1 | 2;
type HorseKindType = 0 | 1;
type HorseDateModeType = 0 | 1 | 2;

export type HorsePedigree = {
    sire: HorseType | null,
    dame: HorseType | null,
}

export type HorseType = {
    id: number
    name: string
    breed: HorseBreedsType | null
    sex: HorseSexType,
    description: string
    age: number | null
    bdate_formatted: string | null
    ddate_formatted: string | null
    photos: GalleryPhotoType[]
    kind?: HorseKindType
    owner?: HorseOwnerType | null
    children?: HorseType[]
    pedigree?: HorsePedigree
    bdate?: string
    ddate?: string
    bdate_mode?: HorseDateModeType
    ddate_mode?: HorseDateModeType
    created_at?: string
    created_by?: string
}

export type HorseTableDataItemType = Omit<HorseType, 'children'>& TableDataItemType & {
    _children?: HorseType[]
}

export type HorseAPIFiltersType = {
    limit?: number
    offset?: number
    name?: string | undefined
    description?: string | undefined
    breed?: number[]
    sex?: number[]
    kind?: number[]
}

export type HorseListResponseType = ApiListPaginatedResponseType<HorseType>

export type HorsePageMetadataType = {
    breedList: FilterListDataType[]
    kindList: FilterListDataType[]
    sexList: FilterListDataType[]
}

export type GetHorseTableColumnsType = (
    filters: HorseAPIFiltersType,
    setFilters: (filtersData: HorseAPIFiltersType) => void,
    pageMetadata: HorsePageMetadataType
) => ColumnType<HorseTableDataItemType>[]
