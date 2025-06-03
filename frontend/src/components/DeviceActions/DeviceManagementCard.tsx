/** Implements the right side of the device management split screen. Allows removing and reconnecting devices. */
import React from "react";
import {Navigate, useLocation} from "react-router-dom";
import getDeviceProps from "./ParseDeviceDetails";
import FanControlMenu from "./FanControlMenu";
import RemoveDeviceCard from "./RemoveDeviceCard";
import ConnectDeviceCard from "./ConnectDeviceCard";


const DeviceManagementCard: React.FC = () => {
    const location = useLocation();
    const data = getDeviceProps(location);
    if (data === null) {
        return <Navigate to='/' replace/>
    }
    const {
        id,
        title,
        mac_address,
        software_version,
        serial_port,
        fan_setting,
        connected,
        src,
        alt,
        maxHeight
    } = data;


    let pageContent = null;
    if (connected === 1) {
        pageContent = <>
            <FanControlMenu/>
            <hr/>
            <RemoveDeviceCard deviceName={title}/>
        </>
    } else if (connected === 2) {
        // Test running
    } else {
        pageContent = <ConnectDeviceCard oldDeviceName={title}/>
    }

    return <div className="bg-gray-50 p-6 rounded-lg shadow-lg">
        <div
            className={`relative bg-white shadow-md rounded-lg overflow-hidden content-center text-center`}>
            <div className="bg-white p-6 rounded-lg shadow-lg">
                {pageContent}
            </div>
        </div>
    </div>
}

export default DeviceManagementCard;