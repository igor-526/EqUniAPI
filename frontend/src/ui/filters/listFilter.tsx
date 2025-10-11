import { Select } from "antd";
import {GetFilterListElementType} from "@/types/filters/filterList";
import {FiltersBaseType} from "@/types/filters/filterBase";

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