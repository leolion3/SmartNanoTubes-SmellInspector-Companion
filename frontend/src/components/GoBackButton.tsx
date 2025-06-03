import React from "react";
import {useNavigate} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowLeft} from "@fortawesome/free-solid-svg-icons";


interface IGoBackButton {
    link: string;
}

const GoBackButton: React.FC<IGoBackButton> = (props) => {
    const navigate = useNavigate();

    const prevPage = () => {
        navigate(props.link);
    }

    const goBack = () => {
        return <button
            onClick={prevPage}
            className="px-6 py-3 bg-transparent text-gray-500 rounded-md text-lg hover:text-gray-800"
            style={{maxWidth: '100px !important', float: 'left'}}
        >
            <FontAwesomeIcon icon={faArrowLeft} className="mr-3"/>
            Zurück
        </button>
    }

    return (<div className="w-full">
        {goBack()}
    </div>);
}

export default GoBackButton;