import React from "react";
import SplitScreenPage from "../../layout/SplitScreenPage";
import SingleScreenPage from "../../layout/SingleScreenPage";
import StartTestCard from "../../components/TestActions/StartTestCard";
import TestDetailsCard from "../../components/TestActions/TestDetailsCard";
import TestManagementCard from "../../components/TestActions/TestManagementCard";
import AverageDataChart from "../../components/Charts/AverageDataChart";


export const TestDetailsPage = () => {
    return (
        <SplitScreenPage
            firstElement={<TestDetailsCard/>}
            secondElement={<TestManagementCard/>}
            additionalElements={<AverageDataChart/>}
            prevPageRef="/tests"/>
    )
}

export const AddTestPage = () => {
    return (
        <SingleScreenPage
            elements={<StartTestCard/>}
            prevPageRef="/tests"/>
    )
}
