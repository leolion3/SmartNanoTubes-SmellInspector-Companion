/** Allows disconnecting connected devices. */
import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faTimes, faTrash} from "@fortawesome/free-solid-svg-icons";
import axiosInstance from "../../authentication/axios-instance";
import {useNavigate} from "react-router-dom";


interface RemoveDeviceCardProps {
    deviceName: string;
}


const RemoveDeviceCard: React.FC<RemoveDeviceCardProps> = ({deviceName}) => {
    const [errorMessage, setErrorMessage] = useState("");
    const [isConfirming, setIsConfirming] = useState(false);
    const navigate = useNavigate();

    async function removeDevice(device_name: string) {
        const payload = {
            device_nickname: device_name
        };
        try {
            const response = await axiosInstance.post('de_register_device', payload);
            if (response.status === 200) {
                navigate('/devices', {state: {message: "Device removed successfully!"}});
            }
        } catch (error) {
            console.log(error);
            setErrorMessage("Gerät ist beschäftigt und kann derzeit nicht getrennt werden.");
            setIsConfirming(false);
        }
    }

    return <div className="bg-white p-6 rounded-lg shadow-lg">
        {isConfirming ? (
            <div className="space-x-2">
                <p className='mb-2'>Sind Sie sicher?</p>
                <button
                    onClick={() => removeDevice(deviceName)}
                    className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                    <FontAwesomeIcon icon={faCheck}/> Trennen
                </button>
                <button
                    onClick={() => setIsConfirming(false)}
                    className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400"
                >
                    <FontAwesomeIcon icon={faTimes}/> Abbrechen
                </button>
            </div>
        ) : (
            <button
                onClick={() => setIsConfirming(true)}
                className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400"
            >
                <FontAwesomeIcon icon={faTrash} className='mr-1'/> Gerät Trennen
            </button>
        )}
        {errorMessage && (
            <div className="text-red-500 mt-4">
                {errorMessage}
            </div>
        )}
    </div>
}

export default RemoveDeviceCard;