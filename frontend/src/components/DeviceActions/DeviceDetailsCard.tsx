/** Displays the device details in the left card of a split screen page. */
import React from "react";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCircle} from "@fortawesome/free-solid-svg-icons";
import {Navigate, useLocation} from "react-router-dom";
import getDeviceProps from "./ParseDeviceDetails";


const DeviceDetailsCard: React.FC = () => {
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
    const statusColor = connected === 1 ? 'green' : 'red';
    const bgColor = connected === 1 ? 'bg-white' : 'bg-gray-200';
    const hoverColor = connected === 1 ? 'hover:bg-gray-200' : 'hover:bg-gray-400';
    const opacity = connected === 1 ? '' : 'opacity-50';
    const hiddenOnDisconnect = connected === 1? 'visible' : 'invisible';
    return <div className="bg-gray-50 p-6 rounded-lg shadow-lg">
        <div
            className={`relative ${bgColor} shadow-md rounded-lg overflow-hidden content-center text-center ${hoverColor} transition-all duration-300`}>
            <div className={`absolute top-2 right-3`}>
                <FontAwesomeIcon icon={faCircle} className={`w-3 h-3`} style={{color: statusColor}}/>
            </div>
            <img
                src={src}
                alt={alt}
                className={`${opacity} mr-auto ml-auto mt-8`} style={{height: `${maxHeight}px`}}
            />
            <div className="p-4 mb-2">
                <h2 className="text-lg font-semibold mb-2">Gerät Name: {title}</h2>
                <p className="text-gray-600">MAC Adresse: {mac_address}</p>
                <p className="text-gray-600">Software Version: {software_version}</p>
                <p className={`text-gray-600 ${hiddenOnDisconnect}`}>Lüfter Stufe: {fan_setting}</p>
                <p className={`text-gray-600 ${hiddenOnDisconnect}`}>Serial Port: {serial_port}</p>
                <p className={`text-gray-600`}>Status: <span className="font-semibold"
                                                             style={{color: statusColor}}>{connected === 1 ? 'Verbunden' : 'Getrennt'}</span>
                </p>
            </div>
        </div>
    </div>;
}

export default DeviceDetailsCard;