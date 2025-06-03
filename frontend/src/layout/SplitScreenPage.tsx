import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowLeft} from "@fortawesome/free-solid-svg-icons";

interface Props {
    firstElement: React.ReactElement;
    secondElement: React.ReactElement;
    additionalElements: any;
    prevPageRef: string;
}

const SplitScreenPage: React.FC<Props> = ({firstElement, secondElement, additionalElements, prevPageRef}) => {
    const goBack = () => {
        return <a href={prevPageRef}
                  className="px-6 py-3 bg-transparent text-gray-500 rounded-md text-lg hover:text-gray-800"
                  style={{maxWidth: '100px !important'}}><FontAwesomeIcon icon={faArrowLeft}
                                                                          className='mr-3'/>Zurück</a>;
    }

    return (
        <div className="flex flex-col bg-gray-100">
            {goBack()}
            <div className="w-full mx-auto pt-2 p-8 justify-center items-center">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {firstElement}
                    {secondElement}
                </div>
                {additionalElements !== undefined ? additionalElements : <></>}
            </div>
        </div>
    )
};

export default SplitScreenPage;