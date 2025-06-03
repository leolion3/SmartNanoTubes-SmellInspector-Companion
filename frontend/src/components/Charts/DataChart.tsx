import React, {Ref, useEffect, useState} from "react";
import {Line} from "react-chartjs-2";
import Legend from "./Legend";

export interface IChartData {
    chartName: string;
    chartData: any;
}


const DataChart: React.FC<IChartData> = ({chartName, chartData}) => {
    const [jitterEnabled, setJitterEnabled] = useState<boolean>(false);
    const [chartDataState, setChartDataState] = useState(chartData);

    const jitter = (value: number) => value + (Math.random() * 0.03) * value;

    const getGraphValues = (data: any[]) => {
        return data.map(value => (jitterEnabled ? jitter(value) : value));
    };

    useEffect(() => {
        if (chartData) {
            const updatedDatasets = chartData.datasets.map((dataset: any) => ({
                ...dataset,
                data: getGraphValues(dataset.data), // Apply jitter if enabled
            }));

            setChartDataState({
                ...chartData,
                datasets: updatedDatasets,
            });
        }
    }, [chartData, jitterEnabled]);

    return <div className='mb-4 relative'>
        <h2 className="text-center font-semibold">{chartName}</h2>
        <div className="absolute top-2 right-2 flex items-center">
            <div
                className={`relative inline-block w-10 h-4 mr-2 cursor-pointer ${jitterEnabled ? 'bg-green-500' : 'bg-gray-300'} rounded-full`}
                onClick={() => setJitterEnabled(!jitterEnabled)}
            >
                <div
                    className={`absolute top-0 left-0 w-4 h-4 bg-white rounded-full shadow transition-transform duration-200 ease-in-out ${jitterEnabled ? 'transform translate-x-6' : ''}`}
                />
            </div>
            <span className="text-gray-700">{jitterEnabled ? 'Jitter On' : 'Jitter Off'}</span>
        </div>
        <div className='h-96'>
            <Line
                data={chartDataState}
                options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 250,
                        easing: 'easeOutCubic',
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: "Data Points",
                            },
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: "Resistance (Ohm)",
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                }}
            />
        </div>
        <Legend datasets={chartDataState.datasets}/>
    </div>
}

export default DataChart