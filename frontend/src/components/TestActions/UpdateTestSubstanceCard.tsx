import React, {useEffect, useState} from "react";
import axiosInstance from "../../authentication/axios-instance";

interface IUpdateTestSubstanceCardProps {
    testName: string;
}

const UpdateTestSubstanceCard: React.FC<IUpdateTestSubstanceCardProps> = ({testName}) => {
    const [errorMessage, setErrorMessage] = useState<string>('');
    const [infoMessage, setInfoMessage] = useState<string>('');
    const [substance_id, setSubstanceId] = useState<string>('1');
    const [previousSubstanceId, setPreviousSubstanceId] = useState<string>('1'); // air is always initially selected
    const [currentSubstanceName, setCurrentSubstanceName] = useState<string>('air');
    const [substances, setSubstances] = useState([]);

    useEffect(() => {
        axiosInstance.get('get_substances')
            .then(res => {
                if (res.status === 200) {
                    setSubstances(res.data);
                }
            })
            .catch(err => {
                setErrorMessage('Substanzen konnten nicht geladen werden.')
            })
    }, []);

    async function getCurrentSubstance() {
        const payload = {
            test_name: testName
        }
        await axiosInstance.post('get_test_substance', payload)
            .then((res) => {
                if (res.status === 200) {
                    const data = res.data;
                    setCurrentSubstanceName(data.substance + ' ' + data.quantity);
                }
            })
            .catch(e => {
                console.log(e);
            })
    }

    useEffect(() => {
        const fetch = async () => {
            await getCurrentSubstance();
        }
        fetch();
        const intervalId = setInterval(fetch, 2000);
        return () => clearInterval(intervalId);
    }, []);


    async function updateSubstance(e: any) {
        e.preventDefault();
        setErrorMessage('');
        setInfoMessage('Gemessene Substanz wird aktualisiert...')
        const payload = {
            test_name: testName,
            substance_id: substance_id
        }
        await axiosInstance.post('update_test_substance', payload)
            .then(res => {
                if (res.status === 200) {
                    setInfoMessage('Substanz aktualisiert.')
                    // Enabled hot-switching substances
                    const current = substance_id;
                    setSubstanceId(previousSubstanceId);
                    setPreviousSubstanceId(current);
                }
            })
            .catch(err => {
                setErrorMessage('Substanz konnte nicht aktualisiert werden.')
                console.log(err)
            })
    }

    return (<form onSubmit={updateSubstance}
                  className="w-full bg-gray-50 max-w-sm mx-auto shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <p className="text-gray-700 font-bold text-lg">Gemessene Substanz Ändern</p>
            <p className="text-gray-700 font-light text-lg mt-1">Aktuell: <span className='font-bold underline'>{currentSubstanceName}</span></p>
            <div className="mb-4 mt-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="device-name">
                    Neue Substanz
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Welche Substanz nun unter den Sensor gestellt wird (oder Luft, wenn keine)">
                            (?)
                          </span>
                </label>
                {substances.length > 0 &&
                    <select
                        id="communication-port"
                        value={substance_id}
                        onChange={(e) => setSubstanceId(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        required
                    >
                        {substances.map(substance => (
                            <option key={substance[0]} value={substance[0]}>{substance[1]} {substance[2]}</option>
                        ))}
                    </select>}
            </div>
            {substances.length > 1 ? <div className="items-center justify-between">
                <button
                    type="submit"
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    Gemessene Substanz ändern
                </button>
            </div> : <div className='font-semibold text-red-500 text-center'>
                Es wurden noch keine Substanzen angelegt.
            </div>}
            {infoMessage && (
                <div className="text-gray-500 mt-4">
                    {infoMessage}
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

export default UpdateTestSubstanceCard;