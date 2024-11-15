
import { Routes, Route } from 'react-router-dom';
import Home from '../pages/landing/Home';
import Login from '../pages/authentication/Login';
import Register from '../pages/authentication/Register';
import ForgotPassword from '../pages/authentication/ForgotPassword';
import ResetPassword from '../pages/authentication/ResetPassword';
import Overview from '../pages/dashboard/Overview';
import PageNotFound from "../pages/authentication/PageNotFound";

function ApplicationRoutes({ assets }) {
    return (
        <Routes>
            <Route path="/" element={<Home assets={assets}/>} />
            <Route path="/login" element={<Login assets={assets}/>} />
            <Route path="/register" element={<Register assets={assets}/>} />
            <Route path="/forgot-password" element={<ForgotPassword assets={assets}/>} />
            <Route path="/reset-password/:token" element={<ResetPassword assets={assets}/>} />
            <Route path="/dashboard/overview" element={<Overview assets={assets}/>} />
            {/* <Route path="/dashboard/algorithm" element={<Algo assets={assets}/>} /> */}
            <Route path="*" element={<PageNotFound assets={assets}/>} />
            {/* Other router */}
        </Routes>
    );
}

export default ApplicationRoutes;