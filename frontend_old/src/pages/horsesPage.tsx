import {useEffect, useState} from 'react';
import {useDispatch} from "react-redux";
import {setNewTitle} from "../store/layoutSlice.js";
import TableWithFilters from "../components/tableWithFilters.tsx";
import TablePagination from "../components/pagination.tsx";
import {getHorsesTableColumns} from "../components/horses/horsesTableColumns";
import {getHorsesList} from "../axios/horsesApi";
import type {HorseAPIFiltersType, HorsePageMetadataType, HorseTableDataItemType, HorseType} from "../types/horsesTypes";
import {getBreedList} from "../axios/breedsApi";
import type {HorseBreedsType} from "../types/horseBreedTypes";
import type {FilterListDataType} from "../types/filterTypes/filterListTypes";

const HorsesPage = () => {
    const dispatch = useDispatch();
    const [filters, setFilters] = useState<HorseAPIFiltersType>({
        limit: 10,
        offset: 0,
        name: undefined,
        description: undefined,
        breed: [],
        sex: [],
        kind: []
    });
    const [loading, setLoading] = useState<boolean>(false);
    const [horsesData, setHorsesData] = useState<HorseTableDataItemType[]>([]);
    const [horsesDataCount, setHorsesDataCount] = useState<number>(0);
    const [pageMetadata, setPageMetadata] = useState<HorsePageMetadataType>({
        breedList: [],
        kindList: [],
        sexList: [],
    });

    const horsesTableColumns = getHorsesTableColumns(filters, setFilters, pageMetadata);

    const headerElements = <>
        <div className="flex items-end">
            <TablePagination
                setFilters={setFilters}
                total={horsesDataCount}
            />
        </div>
    </>

    const onExpandedHorse = (horseRecord: HorseTableDataItemType) => {
        horseRecord._children
        return (
            <div>ТУТ БУДЕТ ТАБЛИЦА С РОДИТЕЛЯМИ И ДЕТЬМИ И ДЕЙСТВИЯМИ С РОДОСЛОВНОЙ</div>
        )
    }

    useEffect(() => {
        setLoading(true);
        getHorsesList(filters).then(data => {
            setHorsesDataCount(data.data.count)
            setHorsesData(
                data.data.items.map(
                    (item: HorseType) => ({
                        ...item,
                        key: item.id.toString(),
                        _children: item.children,
                        children: undefined
                    })
                )
            );
            setLoading(false)
        })
    }, [filters]);
    useEffect(() => {
        dispatch(setNewTitle("Лошади"));
        const sexFilterValues: FilterListDataType[] = [
            {
                label: "Кобыла",
                value: 0,
                key: "0",
            },
            {
                label: "Жеребец",
                value: 1,
                key: "1",
            },
            {
                label: "Мерин",
                value: 2,
                key: "2",
            }
        ]

        const kindFilterValues: FilterListDataType[] = [
            {
                label: "Лошадь",
                value: 0,
                key: "0",
            },
            {
                label: "Пони",
                value: 1,
                key: "1",
            }
        ]
        getBreedList({}).then(data => {
            const breedsFilterList: FilterListDataType[] = data.data.items.map(
                (breed: HorseBreedsType) => ({
                    key: breed.id.toString(),
                    label: breed.name,
                    value: breed.id
                })
            )
            setPageMetadata(
                {
                    breedList: breedsFilterList,
                    kindList: kindFilterValues,
                    sexList: sexFilterValues
                }
            )
        })
    }, []);

    return (
        <>
            <TableWithFilters
                tableColumns={horsesTableColumns}
                tableData={horsesData}
                tableLoading={loading}
                filtersElements={headerElements}
                // onRowListener={onRowListener}
                expandable={{
                    expandedRowRender: (record: HorseTableDataItemType) => onExpandedHorse(record),
                }}
            />
        </>
    )
}

export default HorsesPage;