import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import React from "react";
import {faCircle} from "@fortawesome/free-solid-svg-icons";


interface IPictureWithTextCard {
    id: number;
    src: string;
    alt: string;
    title: string;
    description: string;
    maxHeight: number;
    connected: number;
    showStatus: boolean;
}

const PictureWithTextCard = (props: IPictureWithTextCard) => {
    const statusColor = props.connected === 1 ? 'green' : 'red';
    const visible = props.showStatus ? 'visible' : 'invisible';
    const bgColor = props.showStatus ? props.connected === 1 ? 'bg-white' : 'bg-gray-200' : 'bg-white';
    const hoverColor = props.showStatus ? props.connected === 1 ? 'hover:bg-gray-200' : 'hover:bg-gray-400' : 'hover:bg-gray-200';
    const opacity = props.showStatus ? props.connected === 1 ? '' : 'opacity-50' : '';
    return (<div key={props.id}
                 className={`relative ${bgColor} shadow-md rounded-lg overflow-hidden content-center text-center ${hoverColor} transition-all duration-300`}>
        <div className={`absolute top-2 right-3 ${visible}`}>
            <FontAwesomeIcon icon={faCircle} className={`w-3 h-3`} style={{color: statusColor}}/>
        </div>
        <img src={props.src} alt={props.alt} className={`${opacity} mr-auto ml-auto mt-8`} style={{height: `${props.maxHeight}px`}}/>
        <div className="p-4 mb-2">
            <h2 className="text-lg font-semibold">{props.title}</h2>
            <p className="text-gray-600">{props.description}</p>
        </div>
    </div>);
}

export default PictureWithTextCard;