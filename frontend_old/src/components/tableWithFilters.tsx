import {useEffect, useRef, useState} from 'react';
import { Table } from "antd";
import { createStyles } from 'antd-style';
import type {GetTableWithFiltersElement} from "../types/tableTypes.ts";

const TableWithFilters: GetTableWithFiltersElement = ({tableColumns=[],
                                                          tableData=[],
                                                          tableLoading=true,
                                                          filtersElements=undefined,
                                                          onRowListener=undefined,
                                                          expandable=undefined}) => {
    const useStyle = createStyles(({ css, token }) => {
        // @ts-ignore
        const { antCls } = token;
        return {
            customTable: css`
                ${antCls}-table {
                    ${antCls}-table-container {
                        ${antCls}-table-body,
                        ${antCls}-table-content {
                            scrollbar-width: thin;
                            scrollbar-color: #eaeaea transparent;
                            scrollbar-gutter: stable;
                        }
                    }
                }
            `,
        };
    });
    const { styles } = useStyle();

    const containerRef = useRef<HTMLDivElement | null>(null);
    const filtersRef = useRef<HTMLDivElement | null>(null);
    const [tableHeight, setTableHeight] = useState<number>(400);

    useEffect(() => {
        const updateTableHeight = () => {
            if (containerRef.current && filtersRef.current) {
                const containerRect = containerRef.current.getBoundingClientRect()
                const filtersRect = filtersRef.current.getBoundingClientRect()
                const newHeight = containerRect.height - filtersRect.height - 50
                setTableHeight(Math.max(200, newHeight))
            }
        };

        updateTableHeight();
        window.addEventListener('resize', updateTableHeight);

        return () => window.removeEventListener('resize', updateTableHeight);
    }, []);


    return (
        <div className="h-full overflow-y-hidden" ref={containerRef}>
            {filtersElements &&
                <div ref={filtersRef} className="flex mb-3 justify-between flex-wrap">{filtersElements}</div>}
            <Table
                className={styles.customTable}
                columns={tableColumns}
                dataSource={tableData}
                loading={tableLoading}
                scroll={{y: tableHeight}}
                pagination={false}
                size="small"
                onRow={onRowListener}
                expandable={expandable}
            />
        </div>
    )
}

export default TableWithFilters;