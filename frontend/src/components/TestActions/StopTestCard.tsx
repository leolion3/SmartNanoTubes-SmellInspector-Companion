/** Allows disconnecting connected devices. */
import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faStop, faTimes, faTrash} from "@fortawesome/free-solid-svg-icons";
import axiosInstance from "../../authentication/axios-instance";
import {useNavigate} from "react-router-dom";


interface StopTestCardProps {
    testName: string;
    deviceName: string;
}


const StopTestCard: React.FC<StopTestCardProps> = ({testName, deviceName}) => {
    const [errorMessage, setErrorMessage] = useState("");
    const [infoMessage, setInfoMessage] = useState("");
    const [isConfirming, setIsConfirming] = useState(false);
    const navigate = useNavigate();

    async function stopTest() {
        const payload = {
            test_name: testName,
            device_nickname: deviceName
        };
        try {
            setErrorMessage('');
            setInfoMessage('Test wird gestoppt, bitte warten...')
            const response = await axiosInstance.post('start_stop_test', payload);
            if (response.status === 200) {
                navigate('/tests', {state: {message: "Test erfolgreich gestoppt!"}});
            }
        } catch (error) {
            setErrorMessage("Test konnte nicht gestoppt werden.");
            console.log(error);
        }
    }

    return <div className="bg-white p-6 rounded-lg shadow-lg">
        {isConfirming ? (
            <div className="space-x-2">
                <p className='mb-2'>Sind Sie sicher?</p>
                <button
                    onClick={() => stopTest()}
                    className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                    <FontAwesomeIcon icon={faCheck}/> Stoppen
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
                <FontAwesomeIcon icon={faStop} className='mr-1'/> Test Stoppen
            </button>
        )}
        {errorMessage && (
            <div className="text-red-500 mt-4">
                {errorMessage}
            </div>
        )}
        {infoMessage && (
            <div className="text-gray-500 mt-4">
                {infoMessage}
            </div>
        )}
    </div>
}

export default StopTestCard;