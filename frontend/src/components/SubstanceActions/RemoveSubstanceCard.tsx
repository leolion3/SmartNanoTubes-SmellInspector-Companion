/** Allows disconnecting connected devices. */
import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faTimes, faTrash} from "@fortawesome/free-solid-svg-icons";
import axiosInstance from "../../authentication/axios-instance";
import {useNavigate} from "react-router-dom";


interface IRemoveSubstanceCard {
    substance_id: string;
}


const RemoveSubstanceCard: React.FC<IRemoveSubstanceCard> = ({substance_id}) => {
    const [errorMessage, setErrorMessage] = useState("");
    const [isConfirming, setIsConfirming] = useState(false);
    const navigate = useNavigate();

    async function removeSubstance() {
        const payload = {
            substance_id: substance_id
        };
        try {
            const response = await axiosInstance.post('delete_substance', payload);
            if (response.status === 200) {
                navigate('/substances', {state: {message: "Substance removed successfully!"}});
            }
        } catch (error) {
            setErrorMessage("Substanz kann nicht gelöscht werden.");
            setIsConfirming(false);
        }
    }

    return <div className="bg-white p-6 rounded-lg shadow-lg">
        {isConfirming ? (
            <div className="space-x-2">
                <p className='mb-2'>Sind Sie sicher?</p>
                <button
                    onClick={() => removeSubstance()}
                    className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                    <FontAwesomeIcon icon={faCheck}/> Löschen
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
                <FontAwesomeIcon icon={faTrash} className='mr-1'/> Substanz löschen
            </button>
        )}
        {errorMessage && (
            <div className="text-red-500 mt-4">
                {errorMessage}
            </div>
        )}
    </div>
}

export default RemoveSubstanceCard;