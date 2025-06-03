/** Allows reconnecting disconnected devices. */
import React, {useEffect, useState} from "react";
import axiosInstance from "../../authentication/axios-instance";
import {useNavigate} from "react-router-dom";


interface ConnectDeviceCardProps {
    oldDeviceName: string;
}

const ConnectDeviceCard: React.FC<ConnectDeviceCardProps> = ({oldDeviceName}) => {
    const [errorMessage, setErrorMessage] = useState("");
    const [deviceName, setNewDeviceName] = useState("");
    const [communicationPort, setCommunicationPort] = useState("");
    const [communicationPorts, setCommunicationPorts] = useState([]);
    const [deviceStatusMessage, setDeviceStatusMessage] = useState("");
    const [scanningForComPorts, setScanningForComPorts] = useState(true);
    const [alreadyScanned, setAlreadyScanned] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fun = async () => {
            await axiosInstance.get('get_serial_ports')
                .then(res => {
                    if (res.status === 200) {
                        setCommunicationPorts(res.data.ports);
                        setScanningForComPorts(false);
                        if (res.data.ports.length > 0) {
                            setCommunicationPort(res.data.ports[0]);
                        }
                    }
                })
                .catch(e => {
                    setScanningForComPorts(false);
                })
        }
        if (!alreadyScanned) {
            setAlreadyScanned(true);
            fun();
        }
    }, []);

    async function handleSubmit(e: any) {
        e.preventDefault();
        const payload = {
            device_nickname: deviceName,
            com_port: communicationPort
        }
        console.log(communicationPorts)
        console.log(communicationPort)
        if (deviceName === "") {
            payload["device_nickname"] = oldDeviceName;
        }
        setErrorMessage('');
        setDeviceStatusMessage('Gerät wird verbunden, bitte warten...')
        await axiosInstance.post('register_device', payload)
            .then(res => {
                navigate('/devices', {state: {message: "Gerät wurde verbunden."}});
            }).catch(err => {
                setErrorMessage('Gerät konnte nicht verbunden werden.')
                console.log(err);
            });
        setDeviceStatusMessage('');
    }

    return (
        <form onSubmit={handleSubmit}
              className="w-full bg-gray-50 max-w-sm mx-auto shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <p className="text-gray-700 font-bold text-lg">Gerät Verbinden</p>
            <div className="mb-4 mt-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="device-name">
                    Neuer Gerät Name
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Spezifiziert den Namen des Geräts. Lassen Sie diesen Leer um den alten Namen wieder zu verwenden.">
                            (?)
                          </span>
                </label>
                <input
                    id="device-name"
                    type="text"
                    value={deviceName}
                    onChange={(e) => setNewDeviceName(e.target.value)}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder={oldDeviceName}
                />
            </div>

            <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="communication-port">
                    Serial Port
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Das Gerät wird über einen COM Serial Port verbunden. Tauchen hier keine auf,
                              so müssen Sie den Treiber erst installieren. Mehr info unter der Info Seite.">
                            (?)
                          </span>
                </label>
                {communicationPorts.length > 0 && !scanningForComPorts && <select
                    id="communication-port"
                    value={communicationPort}
                    onChange={(e) => setCommunicationPort(e.target.value.toString())}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                >
                    {communicationPorts.map(port => (
                        <option key={port} value={port}>{port}</option>
                    ))}
                </select>}
                {communicationPorts.length === 0 && !scanningForComPorts &&
                    <p className='text-red-500'>Keine Geräte verbunden. Bitte Installationsanleitung lesen.</p>}
                {scanningForComPorts && <p className='text-green-700'>Port scan wird durchgeführt, bitte warten...</p>}
            </div>

            <div className="items-center justify-between">
                {!scanningForComPorts && communicationPorts.length > 0 &&
                    <button
                        type="submit"
                        disabled={scanningForComPorts || communicationPorts.length === 0}
                        className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Gerät Verbinden
                    </button>}
            </div>
            {deviceStatusMessage && (
                <div className="text-gray-500 mt-4">
                    {deviceStatusMessage}
                </div>
            )}
            {errorMessage && (
                <div className="text-red-500 mt-4">
                    {errorMessage}
                </div>
            )}
        </form>
    );
}

export default ConnectDeviceCard;