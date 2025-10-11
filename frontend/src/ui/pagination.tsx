import {Pagination} from "antd";
import {GetTablePaginationElementType} from "@/types/filters/pagination";
import {FiltersBaseType} from "@/types/filters/filterBase";


const TablePagination: GetTablePaginationElementType = ({ setFilters, total }) => {
    return (
        <Pagination
            defaultCurrent={1}
            total={total}
            hideOnSinglePage={true}
            onChange = {(current, size) => {
                setFilters((prevState: FiltersBaseType) => ({
                    ...prevState,
                    limit: size,
                    offset: (current - 1) * size
                }))
            }}
        />
    )
}

export default TablePagination