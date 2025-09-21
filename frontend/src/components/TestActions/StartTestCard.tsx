/** Allows reconnecting disconnected devices. */
import React, {useEffect, useState} from "react";
import axiosInstance from "../../authentication/axios-instance";
import {useNavigate} from "react-router-dom";


const StartTestCard: React.FC = () => {
    const [errorMessage, setErrorMessage] = useState("");
    const [testName, setTestName] = useState("");
    const [deviceName, setDeviceName] = useState("");
    const [availableDevices, setAvailableDevices] = useState<any>([]);
    const [testMessage, setTestMessage] = useState("");
    const [cacheDataToDB, setCacheDataToDB] = useState<boolean>(true);
    const navigate = useNavigate();

    async function getAvailableDevices() {
        await axiosInstance.get('get_free_devices')
            .then(res => {
                if (res.status === 200) {
                    const deviceNames: any[] = [];
                    res.data.forEach((item: string[5]) => {
                        deviceNames.push(<option value={`${item[1]}`}>{item[1]}</option>);
                    })
                    setAvailableDevices(deviceNames);
                }
            }).catch(e => {
                console.error(e);
            })
    }

    useEffect(() => {
        const fetch = async () => {
            await getAvailableDevices();
        }
        fetch();
        const intervalId = setInterval(fetch, 2000);
        return () => clearInterval(intervalId);
    }, []);

    async function handleSubmit(e: any) {
        e.preventDefault();
        const payload = {
            test_name: testName,
            device_nickname: deviceName,
            data_acquisition_enabled: cacheDataToDB
        }
        setErrorMessage('');
        setTestMessage('Test wird gestartet, bitte warten...')
        await axiosInstance.post('start_stop_test', payload)
            .then(res => {
                navigate('/tests', {state: {message: "Test gestartet."}});
            }).catch(err => {
                setErrorMessage('Test konnte nicht gestartet werden.')
                console.log(err);
            });
        setTestMessage('');
    };
    return (
        <form onSubmit={handleSubmit}
              className="w-full bg-gray-50 max-w-sm mx-auto shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <p className="text-gray-700 font-bold text-lg">Test Starten</p>
            <div className="mb-4 mt-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="test-name">
                    Test Name
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Test name, kann willkürlich gewählt werden und dient nur zur Identifikation der Datensätze.">
                            (?)
                          </span>
                </label>
                <input
                    id="test-name"
                    type="text"
                    value={testName}
                    onChange={(e) => setTestName(e.target.value)}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Test name"
                />
            </div>

            <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="chosen-device">
                    Gewähltes Gerät
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Das Gerät welches den Test durchführen soll.">
                            (?)
                          </span>
                </label>
                <select
                    id="chosen-device"
                    value={deviceName}
                    onChange={(e) => setDeviceName(e.target.value)}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                >
                    <option value="" disabled>Gerät Auswählen</option>
                    {availableDevices}
                </select>
            </div>
            <div className="mb-4 flex flex-wrap text-center space-x-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="chosen-device">
                    Test-Daten Abspeichern?
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Ob aufgenommene Test-Daten in der Datenbank gespeichert werden sollen.">
                            (?)
                          </span>
                </label>
                <input
                    id="enable_data_acquisition_switch"
                    type="checkbox"
                    checked={cacheDataToDB}
                    onChange={(e) => setCacheDataToDB(e.target.checked)}
                    className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer"
                />
            </div>

            <div className="items-center text-center justify-between">
                <button
                    type="submit"
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    Test Starten
                </button>
            </div>
            {testMessage && (
                <div className="text-gray-500 mt-4">
                    {testMessage}
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

export default StartTestCard;