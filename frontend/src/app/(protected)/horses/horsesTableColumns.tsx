import {Table} from "antd";
import {FilterOutlined, SearchOutlined} from "@ant-design/icons";
import {GetHorseTableColumnsType, HorseTableDataItemType} from "@/types/api/horse";
import StringFilter from "@/ui/filters/stringFilter";
import ListFilter from "@/ui/filters/listFilter";

export const getHorsesTableColumns: GetHorseTableColumnsType = (
    filters, setFilters, pageMetadata) => {

    return [
        {
            title: 'Кличка',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.name}</span>
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
                    placeHolder="Поиск по кличке"/>
                </div>
            </>,
        },
        {
            title: 'Порода',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.breed ? record.breed.name : "Отсутствует"}</span>
                    </>
                )
            },
            key: 'breed',
            filterIcon: <FilterOutlined style={{ color: filters.breed?.length ? '#1677ff' : undefined }}/>,
            filterDropdown:
            <div style={{ padding: 8, minWidth: 250 }}>
                <ListFilter
                    filters={filters}
                    setFilters={setFilters}
                    filterKey="breed"
                    filterData={pageMetadata.breedList}
                    placeHolder="Выберите породы"
                />
            </div>
        },
        {
            title: 'Пол',
            render: (record: HorseTableDataItemType) => {
                let sex = ""

                switch (record.sex) {
                    case 0:
                        sex = "Кобыла"
                        break
                    case 1:
                        sex = "Жеребец"
                        break
                    case 2:
                        sex = "Мерин"
                        break
                }

                return (
                    <>
                        <span>{sex}</span>
                    </>
                )
            },
            key: 'sex',
            filterIcon: <FilterOutlined style={{ color: filters.sex?.length ? '#1677ff' : undefined }}/>,
            filterDropdown:
                <div style={{ padding: 8, minWidth: 250 }}>
                    <ListFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="sex"
                        filterData={pageMetadata.sexList}
                        placeHolder="Выберите пол"
                    />
                </div>
        },
        {
            title: 'Описание',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.description}</span>
                    </>
                )
            },
            key: 'description',
            filterIcon: <SearchOutlined style={{ color: filters.description ? '#1677ff' : undefined }} />,
            filterDropdown: <>
                <div style={{ padding: 8 }}>
                    <StringFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="description"
                        placeHolder="Поиск по описанию"/>
                </div>
            </>,
        },
        {
            title: 'Возраст',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.age}</span>
                    </>
                )
            },
            key: 'age',
        },
        {
            title: 'Дата рождения',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.bdate_formatted}</span>
                    </>
                )
            },
            key: 'bdate_formatted',
        },
        {
            title: 'Дата смерти',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.ddate_formatted}</span>
                    </>
                )
            },
            key: 'ddate_formatted',
        },
        Table.EXPAND_COLUMN,
        {
            title: 'Родословная',
            render: (record: HorseTableDataItemType) => {
                let sire = false
                let dame = false
                let _children: number | undefined = 0

                sire = record.pedigree?.sire !== null
                dame = record.pedigree?.dame !== null
                _children = record._children?.length

                return (
                    <>
                        {sire && <span>Мать </span>}
                        {dame && <span>Отец </span>}
                        {_children && <span>{_children} детей</span>}
                    </>
                )
            },
            key: 'pedigree',
        },
        {
            title: 'Фото',
            render: (record: HorseTableDataItemType) => {
                return (
                    <>
                        <span>{record.photos.length}</span>
                    </>
                )
            },
            key: 'photos_count',
        },
        {
            title: 'Тип',
            render: (record: HorseTableDataItemType) => {
                let kind = ""

                switch (record.kind) {
                    case 0:
                        kind = "Лошадь"
                        break
                    case 1:
                        kind = "Пони"
                        break
                }

                return (
                    <>
                        <span>{kind}</span>
                    </>
                )
            },
            key: 'horse_type',
            filterIcon: <FilterOutlined style={{ color: filters.kind?.length ? '#1677ff' : undefined }}/>,
            filterDropdown:
                <div style={{ padding: 8, minWidth: 250 }}>
                    <ListFilter
                        filters={filters}
                        setFilters={setFilters}
                        filterKey="kind"
                        filterData={pageMetadata.kindList}
                        placeHolder="Выберите тип"
                    />
                </div>
        },
    ]
}