import React, {useState} from "react";
import axiosInstance from "../../authentication/axios-instance";
import {useNavigate} from "react-router-dom";

interface UpdateSubstanceCardProps {
    substance_id: string;
    substance_name: string;
    substance_quantity: string;
}

const UpdateSubstanceCard: React.FC<UpdateSubstanceCardProps> = (
    {substance_id, substance_name, substance_quantity}
) => {
    const [errorMessage, setErrorMessage] = useState<string>('');
    const [infoMessage, setInfoMessage] = useState<string>('');
    const [substanceName, setSubstanceName] = useState<string>('');
    const [substanceQuantity, setSubstanceQuantity] = useState<string>('');
    const navigate = useNavigate();

    async function updateSubstanceDetails(e: any) {
        e.preventDefault();
        setErrorMessage('');
        setInfoMessage('Substanz wird aktualisiert...')
        const payload = {
            substance_id: substance_id,
            substance_name: substanceName,
            substance_quantity: substanceQuantity
        }
        await axiosInstance.post('update_substance', payload)
            .then(res => {
                if (res.status === 200) {
                    setInfoMessage('Substanz aktualisiert.')
                    navigate('/substances', {state: {message: "Substanz wurde aktualisiert."}});
                }
            })
            .catch(err => {
                setErrorMessage('Substanz konnte nicht aktualisiert werden.')
                setInfoMessage('');
                console.log(err);
            })
    }

    return (<form onSubmit={updateSubstanceDetails}
                  className="w-full bg-gray-50 max-w-sm mx-auto shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <p className="text-gray-700 font-bold text-lg">Substanz-Daten Ändern</p>
            <div className="mb-4 mt-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="substance-name">
                    Neuer Substanz-Name
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Wie die Substanz heißen soll.">
                            (?)
                          </span>
                </label>
                <input
                    id="substance-name"
                    type="text"
                    value={substanceName}
                    onChange={(e) => setSubstanceName(e.target.value)}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder={substance_name !== ' ' ? substance_name : 'Substanz-Name'}
                />
            </div>
            <div className="mb-4 mt-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="substance-quantity">
                    Neue Substanz-Menge (ml)
                    <span className="ml-2 text-gray-500 cursor-pointer"
                          title="Die Menge der gemessenen Substanz, z.B. in ml.">
                            (?)
                          </span>
                </label>
                <input
                    id="substance-quantity"
                    type="text"
                    value={substanceQuantity}
                    onChange={(e) => setSubstanceQuantity(e.target.value)}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder={substance_quantity !== ' ' ? substance_quantity : 'Substanz-Menge'}
                />
            </div>
            <div className="items-center justify-between">
                <button
                    type="submit"
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    Substanz Aktualisieren
                </button>
            </div>
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

export default UpdateSubstanceCard;