import React from "react";
import {Dataset} from "./IChartData";


const Legend: React.FC<{ datasets: Dataset[] }> = ({datasets}) => (
    <div className='shadow mt-2 p-1 mb-4 bg-white'>
        <div className="flex flex-wrap justify-center mt-2">
            {datasets.map((dataset, index) => (
                <div key={index} className="flex items-center mr-4 mb-2">
                    <span
                        className="w-4 h-4 mr-2 inline-block rounded"
                        style={{backgroundColor: dataset.borderColor}}
                    ></span>
                    <span>{dataset.label}</span>
                </div>
            ))}
        </div>
    </div>
);

export default Legend;