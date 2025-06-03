/** Implements the right side of the substance management split screen. Allows adding, removing and updating substances. */
import React from "react";
import {Navigate, useLocation} from "react-router-dom";
import getSubstanceDetails from "./ParseSubstanceDetails";
import RemoveSubstanceCard from "./RemoveSubstanceCard";
import UpdateSubstanceCard from "./UpdateSubstanceCard";
import AddSubstanceCard from "./AddSubstanceCard";

interface ISubstanceManagementCard {
    new_entry: boolean;
}

const SubstanceManagementCard: React.FC<ISubstanceManagementCard> = ({new_entry}) => {
    const location = useLocation();
    const data = getSubstanceDetails(location);
    if (data === null) {
        return <Navigate to='/' replace/>
    }
    const {
        title,
        substance_id,
        substance_name,
        substance_quantity,
        maxHeight
    } = data;


    let pageContent = null;
    if (new_entry) {
        pageContent = <AddSubstanceCard/>
    } else {
        pageContent = <>
            <UpdateSubstanceCard substance_id={substance_id} substance_name={substance_name}
                                 substance_quantity={substance_quantity}/>
            <hr/>
            <RemoveSubstanceCard substance_id={substance_id}/>
        </>
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

export default SubstanceManagementCard;