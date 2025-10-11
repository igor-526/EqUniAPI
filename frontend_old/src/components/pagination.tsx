import {Pagination} from "antd";
import type {GetTablePaginationElementType} from "../types/paginationTypes.ts";
import type {FiltersBaseType} from "../types/filterBaseTypes.ts";

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