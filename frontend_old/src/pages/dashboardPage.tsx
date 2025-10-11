import {useDispatch} from "react-redux";
import {setNewTitle} from "../store/layoutSlice.js";
import {useEffect} from "react";

const DashboardPage = () => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(setNewTitle("Дэшборд"));
    }, []);

    return (
        <>
            <div>Добро пожаловать</div>
        </>
    )
}

export default DashboardPage;