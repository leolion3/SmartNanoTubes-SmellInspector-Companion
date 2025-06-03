import React from "react";
import SplitScreenPage from "../../layout/SplitScreenPage";
import DeviceDetailsCard from "../../components/DeviceActions/DeviceDetailsCard";
import DeviceManagementCard from "../../components/DeviceActions/DeviceManagementCard";
import SingleScreenPage from "../../layout/SingleScreenPage";
import SubstanceDetailsCard from "../../components/SubstanceActions/SubstanceDetailsCard";
import SubstanceManagementCard from "../../components/SubstanceActions/SubstanceManagementCard";


export const SubstanceDetailsPage = () => {
    return (
        <SplitScreenPage
            firstElement={<SubstanceDetailsCard />}
            secondElement={<SubstanceManagementCard new_entry={false}/>}
            additionalElements={undefined}
            prevPageRef="/substances"/>
    )
}

export const AddSubstancePage = () => {
    return (
        <SingleScreenPage
            elements={<SubstanceManagementCard new_entry={true}/>}
            prevPageRef="/substances"/>
    )
}
