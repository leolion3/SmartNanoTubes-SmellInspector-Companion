/** Implements the test add/update/remove right-side of the test split-screen page */
import React, {useState} from "react";
import {Navigate, useLocation} from "react-router-dom";
import getTestDetails from "./ParseTestDetails";
import StopTestCard from "./StopTestCard";
import UpdateTestSubstanceCard from "./UpdateTestSubstanceCard";


const TestManagementCard: React.FC = () => {
    const location = useLocation();
    const data = getTestDetails(location);
    if (data === null) {
        return <Navigate to='/' replace/>
    }
    const {
        title,
        device_name,
        maxHeight
    } = data;

    return <div className="bg-gray-50 p-6 rounded-lg shadow-lg">
        <div
            className={`relative bg-white shadow-md rounded-lg overflow-hidden content-center text-center`}>
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <UpdateTestSubstanceCard testName={title} />
                <hr/>
                <StopTestCard testName={title} deviceName={device_name} />
            </div>
        </div>
    </div>
}

export default TestManagementCard;