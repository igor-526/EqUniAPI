import { Select } from "antd";
import type {GetFilterListElementType} from "../../types/filterTypes/filterListTypes";
import type {FiltersBaseType} from "../../types/filterTypes/filterBaseTypes";

const ListFilter: GetFilterListElementType = ({ filters,
                                                  setFilters,
                                                  filterKey,
                                                  filterData,
                                                  placeHolder="Выберите"}) => {
    return (
        <Select
            mode="multiple"
            allowClear
            style={{ marginBottom: 8, display: 'block' }}
            placeholder={placeHolder}
            value={filters[filterKey]}
            onChange={(e) => {
                setFilters((prevState: FiltersBaseType) => ({
                    ...prevState,
                    [filterKey]: e
                }))}}
            options={filterData}
        />
    )
}

export default ListFilter