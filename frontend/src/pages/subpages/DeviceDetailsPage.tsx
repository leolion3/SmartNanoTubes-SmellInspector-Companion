import React from "react";
import SplitScreenPage from "../../layout/SplitScreenPage";
import DeviceDetailsCard from "../../components/DeviceActions/DeviceDetailsCard";
import DeviceManagementCard from "../../components/DeviceActions/DeviceManagementCard";
import SingleScreenPage from "../../layout/SingleScreenPage";


export const DeviceDetailsPage = () => {
    return (
        <SplitScreenPage
            firstElement={<DeviceDetailsCard />}
            secondElement={<DeviceManagementCard/>}
            additionalElements={undefined}
            prevPageRef="/devices"/>
    )
}

export const AddDevicePage = () => {
    return (
        <SingleScreenPage
            elements={<DeviceManagementCard/>}
            prevPageRef="/devices"/>
    )
}
