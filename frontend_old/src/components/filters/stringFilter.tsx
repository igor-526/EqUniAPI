import {Button, Input, Space} from "antd";
import type {GetFilterStringElementType} from "../../types/filterTypes/filterStringTypes";
import type {FiltersBaseType} from "../../types/filterTypes/filterBaseTypes";
import ClearIcon from '@mui/icons-material/Clear';

const StringFilter: GetFilterStringElementType = ({ filters, setFilters, filterKey, placeHolder="Поиск" }) => {
    return (
        <>
            <Input
                placeholder={placeHolder}
                value={filters[filterKey]}
                onChange={(e) => setFilters((prevState: FiltersBaseType) => ({
                    ...prevState,
                    [filterKey]: e.target.value.trim() ? e.target.value.trim() : null
                }))}
                style={{ marginBottom: 8, display: 'block' }}
            />
            <Space>
                <Button
                    size="small"
                    color="danger"
                    variant="outlined"
                    onClick={() => {
                        setFilters((prevState: FiltersBaseType) => ({
                            ...prevState,
                            [filterKey]: null
                        }))
                    }}
                >
                    <ClearIcon /> Очистить
                </Button>
            </Space>
        </>
    )
}

export default StringFilter