import {ConfigProvider} from "antd";
import ru_RU from 'antd/lib/locale/ru_RU';
import { Provider } from 'react-redux';
import {store} from './store';
import AppRoutes from "./routes/routes.tsx";

const App = () => {
    return (
        <Provider store={store}>
            <ConfigProvider locale={ru_RU}>
                    <AppRoutes />
            </ConfigProvider>
        </Provider>
    );
};
export default App;