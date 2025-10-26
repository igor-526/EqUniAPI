import { SearchOutlined } from "@ant-design/icons";
import StringFilter from "@/ui/filters/stringFilter";
import ListFilter from "@/ui/filters/listFilter";
import { GetStaticInformationTableColumnsType, StaticInformationTableDataItemType } from "@/types/api/static_information";
import { FilterListDataType } from "@/types/filters/filterList";

const availableAsType: FilterListDataType[] = [
    {
        label: "string",
        key: "string",
        value: "string"
    },
    {
        label: "number",
        key: "number",
        value: "number"
    },
    {
        label: "float",
        key: "float",
        value: "float"
    },
    {
        label: "boolean",
        key: "boolean",
        value: "boolean"
    },
    {
        label: "json",
        key: "json",
        value: "json"
    },
    {
        label: "date",
        key: "date",
        value: "date"
    },
    {
        label: "time",
        key: "time",
        value: "time"
    },
    {
        label: "datetime",
        key: "datetime",
        value: "datetime"
    }
]

export const getStaticInformationTableColumns: GetStaticInformationTableColumnsType = (
    filters, setFilters) => {
    return [
        {
            title: 'Наименование',
            render: (record: StaticInformationTableDataItemType) => {
                return (
                    <>
                        <span>{record.title}</span>
                    </>
                )
            },
            key: 'title',
            filterIcon: <SearchOutlined style={{ color: filters.title ? '#1677ff' : undefined }} />,
            filterDropdown:
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="title"
                        placeHolder="Поиск по наименованию" />
                </div>
        },
        {
            title: 'Ключ API',
            render: (record: StaticInformationTableDataItemType) => {
                return (
                    <>
                        <span>{record.name}</span>
                    </>
                )
            },
            key: 'name',
            filterIcon: <SearchOutlined style={{ color: filters.name ? '#1677ff' : undefined }} />,
            filterDropdown:
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="name"
                        placeHolder="Поиск по ключу API" />
                </div>
        },
        {
            title: 'Тип данных',
            render: (record: StaticInformationTableDataItemType) => {
                return (
                    <>
                        <span>{record.as_type}</span>
                    </>
                )
            },
            key: 'as_type',
            filterIcon: <SearchOutlined style={{ color: filters.as_type?.length ? '#1677ff' : undefined }} />,
            filterDropdown: <div style={{ padding: 8, minWidth: 250 }}>
                    <ListFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="as_type"
                        filterData={availableAsType}
                        placeHolder="Выберите типы"
                    />
                </div>
        },
        {
            title: 'Значение',
            render: (record: StaticInformationTableDataItemType) => {
                return (
                    <>
                        <span>{record.value}</span>
                    </>
                )
            },
            key: 'as_type',
        }
    ]
}