import {Route, Routes} from "react-router";
import LoginPage from "../pages/loginPage.tsx";
import BaseLayout from "../BaseLayout.tsx";
import HorsesPage from "../pages/horsesPage.tsx";
import DashboardPage from "../pages/dashboardPage.tsx";


const AppRoutes = () => {
    return <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<BaseLayout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/horses" element={<HorsesPage />} />
        </Route>
    </Routes>
}

export default AppRoutes