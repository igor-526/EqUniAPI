"use client"

import { useEffect, useState } from 'react';
import TableWithFilters from "@/ui/tableWithFilters";
import { Button } from 'antd';
import { getStaticInformationTableColumns } from './staticInformationTableColumns';
import { StaticInformationListParamsType, StaticInformationOutDto, StaticInformationTableDataItemType } from '@/types/api/static_information';
import { listStatisticInformation } from '@/api/static_information';
import StaticInformationModal from './staticInformationModal';

const StaticInformationPage: React.FC = () => {
    const [filters, setFilters] = useState<StaticInformationListParamsType>({
        title: undefined,
        name: undefined,
        as_type: [],
    });
    const [loading, setLoading] = useState<boolean>(false);
    const [staticInformationData, setStaticInformationData] = useState<StaticInformationTableDataItemType[]>([]);
    const [staticInformationModalOpen, setStaticInformationModalOpen] = useState<boolean>(false);
    const [selectedStaticInformation, setSelectedStaticInformation] = useState<StaticInformationTableDataItemType | null>(null);

    const staticInformationTableColumns = getStaticInformationTableColumns(filters, setFilters);

    const onNewListener = () => {
        setSelectedStaticInformation(null)
        setStaticInformationModalOpen(true)
    }

    const onRowListener = (record: StaticInformationTableDataItemType) => ({
        onClick: () => {
            setSelectedStaticInformation(record)
            setStaticInformationModalOpen(true)
        }
    })

    const onAction = () => {
        setFilters((prevFilters) => ({
            ...prevFilters
        }));
    }

    const headerElements = <>
        <div className="flex items-end">
            <Button onClick={onNewListener}>Добавить</Button>
        </div>
    </>

    useEffect(() => {
        setLoading(true);
        listStatisticInformation(filters).then(data => {
            setStaticInformationData(
                data.data.map(
                    (item: StaticInformationOutDto) => ({
                        ...item,
                        key: item.id.toString(),
                    })
                )
            );
            setLoading(false)
        })
    }, [filters]);

    useEffect(() => {
        if (!staticInformationModalOpen && selectedStaticInformation !== null) {
            setSelectedStaticInformation(null);
        }
    }, [staticInformationModalOpen, selectedStaticInformation]);

    return (
        <>
            <TableWithFilters
                tableColumns={staticInformationTableColumns}
                tableData={staticInformationData}
                tableLoading={loading}
                filtersElements={headerElements}
                onRowListener={onRowListener}
            />
            <StaticInformationModal
                staticInformationModalOpen={staticInformationModalOpen}
                setStaticInformationModalOpen={setStaticInformationModalOpen}
                selectedStaticInformation={selectedStaticInformation}
                onAction={onAction}
            />
        </>
    )
}

export default StaticInformationPage;
