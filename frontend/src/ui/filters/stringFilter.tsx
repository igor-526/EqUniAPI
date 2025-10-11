import {Button, Input, Space} from "antd";
import ClearIcon from '@mui/icons-material/Clear';
import {GetFilterStringElementType} from "@/types/filters/filterString";
import {FiltersBaseType} from "@/types/filters/filterBase";

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