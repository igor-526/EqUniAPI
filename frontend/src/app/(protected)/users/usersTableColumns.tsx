import { SearchOutlined } from "@ant-design/icons";
import StringFilter from "@/ui/filters/stringFilter";
import { GetUsersTableColumnsType, UserTableDataItemType } from "@/types/api/users";
import ListFilter from "@/ui/filters/listFilter";

export const getUsersTableColumns: GetUsersTableColumnsType = (
    filters, setFilters, pageMetadata) => {
    return [
        {
            title: 'ФИО',
            render: (record: UserTableDataItemType) => {
                let fullName = `${record.last_name} ${record.first_name}`
                if (record.patronymic) {
                    fullName += ` ${record.patronymic}`
                }
                return (
                    <>
                        <span>{fullName}</span>
                    </>
                )
            },
            key: 'name',
            filterIcon: <SearchOutlined style={{ color: filters.name ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="name"
                        placeHolder="Поиск по ФИО" />
                </div>
            </>,
        },
        {
            title: 'Username',
            render: (record: UserTableDataItemType) => {
                return (
                    <>
                        <span>{record.username}</span>
                    </>
                )
            },
            key: 'username',
            filterIcon: <SearchOutlined style={{ color: filters.username ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="username"
                        placeHolder="Поиск по username" />
                </div>
            </>,
        },
        {
            title: 'Email',
            render: (record: UserTableDataItemType) => {
                return (
                    <>
                        <span>{record.email}</span>
                    </>
                )
            },
            key: 'email',
            filterIcon: <SearchOutlined style={{ color: filters.email ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="email"
                        placeHolder="Поиск по email" />
                </div>
            </>,
        },
        {
            title: 'Группы',
            render: (record: UserTableDataItemType) => {
                return (
                    <>
                        <span>{record.groups}</span>
                    </>
                )
            },
            key: 'groups',
            filterIcon: <SearchOutlined style={{ color: filters.groups?.length ? '#1677ff' : undefined }} />,
            filterDropdown:
                <div style={{ padding: 8, minWidth: 250 }}>
                    <ListFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="groups"
                        filterData={pageMetadata.user_groups}
                        placeHolder="Выберите группы"
                    />
                </div>

        }
    ]
}