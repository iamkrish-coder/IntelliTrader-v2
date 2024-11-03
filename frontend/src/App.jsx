import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from 'sonner';
import PageNotFound from './pages/authentication/PageNotFound';
import ApplicationRoutes from './router/ApplicationRoutes.jsx';
import IMAGES from './constants/images.js';
import VECTORS from './constants/vectors.js';
import ICONS from './constants/icons.js';
import MESSAGES from './constants/messages.js';
import './assets/scss/style.scss';

const constants = {
    IMAGES : IMAGES,
    VECTORS : VECTORS,
    ICONS: ICONS,
    MESSAGES: MESSAGES
}

function App() {
    return (
        <React.Fragment>
            <BrowserRouter>
                <Routes>
                    <Route path="/*" element={<ApplicationRoutes assets={constants}/>} />
                    <Route path="*" element={<PageNotFound />} />
                </Routes>
            </BrowserRouter>
            <Toaster position="top-center" className='p-0.5' richColors />
        </React.Fragment>
    );
}

export default App;
