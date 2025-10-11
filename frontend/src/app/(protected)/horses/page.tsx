"use client"

import {useEffect, useState } from 'react';
import {HorseAPIFiltersType, HorsePageMetadataType, HorseTableDataItemType, HorseType} from "@/types/api/horse";
import {getHorsesTableColumns} from "@/app/(protected)/horses/horsesTableColumns";
import TablePagination from "@/ui/pagination";
import {getHorsesList} from "@/api/horses";
import {FilterListDataType} from "@/types/filters/filterList";
import {getBreedList} from "@/api/breeds";
import {HorseBreedsType} from "@/types/api/horseBreed";
import TableWithFilters from "@/ui/tableWithFilters";

const HorsesPage = () => {
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