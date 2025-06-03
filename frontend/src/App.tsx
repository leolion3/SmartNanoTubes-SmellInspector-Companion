// src/App.tsx

import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Navbar from "./layout/Navbar";
import Footer from "./layout/Footer";
import DashboardPage from "./pages/DashboardPage";
import DevicesPage from "./pages/DevicesPage";
import {AddDevicePage, DeviceDetailsPage} from "./pages/subpages/DeviceDetailsPage";
import TestsPage from "./pages/TestsPage";
import {AddTestPage, TestDetailsPage} from "./pages/subpages/TestDetailsPage";
import SubstancesPage from "./pages/SubstancesPage";
import {AddSubstancePage, SubstanceDetailsPage} from "./pages/subpages/SubstanceDetailsPage";


const App: React.FC = () => {

    return (
        <Router>
            <div className="flex flex-col min-h-screen">
                {/* Navbar */}
                <Navbar/>
                {/* Main content */}
                <div className="flex-grow">
                    <div className="container mx-auto px-4 py-8">
                        <Routes>
                            <Route path="/" element={<DashboardPage/>}/>
                            <Route path="/devices" element={<DevicesPage/>}/>
                            <Route path="/tests" element={<TestsPage/>}/>
                            <Route path="/add-device" element={<AddDevicePage/>}/>
                            <Route path="/device-preview" element={<DeviceDetailsPage/>}/>
                            <Route path="/add-test" element={<AddTestPage/>}/>
                            <Route path="/test-preview" element={<TestDetailsPage/>}/>
                            <Route path="/substances" element={<SubstancesPage/>}/>
                            <Route path="/add-substance" element={<AddSubstancePage/>}/>
                            <Route path="/substance-preview" element={<SubstanceDetailsPage/>}/>
                        </Routes>
                    </div>
                </div>

                {/* Footer */}
                <Footer/>
            </div>
        </Router>
    );
};

export default App;
