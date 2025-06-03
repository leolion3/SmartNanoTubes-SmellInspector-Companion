/** Implements the left view of a substance page split-screen */
import React from "react";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faVial} from "@fortawesome/free-solid-svg-icons";
import {useLocation} from "react-router-dom";
import getSubstanceDetails from "./ParseSubstanceDetails";


const SubstanceDetailsCard: React.FC = () => {
    const location = useLocation();
    const data = getSubstanceDetails(location);

    return <div className="bg-gray-50 p-6 rounded-lg shadow-lg">
        <div
            className={`relative bg-white shadow-md rounded-lg overflow-hidden content-center text-center hover:bg-gray-200 transition-all duration-300`}>
            <FontAwesomeIcon icon={faVial} className="mr-auto ml-auto mt-8" style={{height: `${data?.maxHeight}px`}}/>
            <div className="p-4 mb-2">
                <h2 className="text-lg font-semibold mb-2">Substanz Name: {data?.title}</h2>
                <p className={`text-gray-600`}>Name (Kurz): <span
                    className="font-semibold">{data?.substance_name}</span></p>
                {data?.substance_quantity !== '' &&
                    <p className={`text-gray-600`}>Menge: <span
                        className="font-semibold">{data?.substance_quantity}</span></p>}
            </div>
        </div>
    </div>
}

export default SubstanceDetailsCard;