import type {ApiListPaginatedResponseType} from "./api";
import type {TableColumnType, TableDataItemType} from "../ui/table";
import type { ColumnType } from 'antd/es/table'
import { FilterListDataType } from "../filters/filterList";

type UserAPIFiltersAvailableSortKeysType = "name" | "-name" | "username" | "-username" | "email" | "-email"

export type UserListRequestParamsType = {
    name?: string
    email?: string
    username?: string
    groups?: number[]
    sort?: UserAPIFiltersAvailableSortKeysType[]
    limit?: number
    offset?: number
}

export type UserRegistrationInDtoType = {
    first_name: string,
    last_name: string,
    username: string,
    password: string,
    patronymic?: string,
    email?: string,
    groups?: number[]
}

export type UserOutDtoType = {
    id: number,
    first_name: string,
    last_name: string,
    patronymic: string,
    username: string,
    email: string,
    photo: string,
    groups: number[]
}

export type UserGroupMetadataOutDtoType = {
    id: number,
    name: string,
    title: string
}

export type UserPageMetadataOutDtoType = {
    user_groups: UserGroupMetadataOutDtoType[]
}

export type UserListOutDtoType = ApiListPaginatedResponseType<UserOutDtoType>



export type UserPageMetadataType = {
    user_groups: FilterListDataType[]
}

export type UserTableDataItemType = UserOutDtoType & TableDataItemType

export type GetUsersTableColumnsType = (
    filters: UserListRequestParamsType,
    setFilters: (filtersData: UserListRequestParamsType) => void,
    pageMetadata: UserPageMetadataType
) => ColumnType<UserTableDataItemType>[]
