import React from "react";
import GoBackButton from "../components/GoBackButton";

interface Props {
    elements: React.ReactElement;
    prevPageRef: string;
}

const SingleScreenPage: React.FC<Props> = ({elements, prevPageRef}) => {
    return (
        <div className="flex flex-col bg-gray-100">
            <GoBackButton link={prevPageRef}/>
            <div className="justify-center items-center w-full mx-auto pt-2 p-8">
                <div className="grid grid-cols-1 md:grid-cols-1">
                    {elements}
                </div>
            </div>
        </div>
    )
};

export default SingleScreenPage;