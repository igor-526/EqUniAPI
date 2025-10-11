import type {ReactNode} from "react";

type TableColumnFixedType = "left"

export type TableDataItemType = {
    key: string
}

export type TableColumnType<T> = {
    title: string;
    render?: (record: T) => ReactNode | string;
    key: string
    fixed?: TableColumnFixedType
    filterIcon?: ReactNode
    filterDropdown?: ReactNode
    dataIndex?: string
}

export type TableWithFiltersProps = {
    tableColumns?: TableColumnType<any>[],
    tableData?: any[],
    tableLoading?: boolean,
    filtersElements?: ReactNode,
    onRowListener?: any | undefined,
    expandable?: any | undefined,
}

export type GetTableWithFiltersElement = (props: TableWithFiltersProps) => ReactNode