import React, {useEffect, useState} from "react";
import {io} from "socket.io-client";
import {Chart, LineElement, CategoryScale, LinearScale, PointElement} from "chart.js";
import {serverIP} from "../../authentication/global-vars";
import getTestDetails from "../TestActions/ParseTestDetails";
import {useLocation} from "react-router-dom";
import {Dataset} from "./IChartData";
import DataChart from "./DataChart";

Chart.register(LineElement, CategoryScale, LinearScale, PointElement);

const RealTimeChart: React.FC = () => {
    const location = useLocation();
    const data = getTestDetails(location);
    const [socket, setSocket] = useState<any>(null);

    const maxDataPoints = 100;
    const test_title = data?.title;

    const initialDatasets: Dataset[] = Array.from({length: 64}, (_, i) => ({
        label: `Sensor ${i + 1}`,
        data: Array(0).fill(100),
        borderColor: `hsl(${(i * 360) / 64}, 70%, 50%)`,
        backgroundColor: `hsla(${(i * 360) / 64}, 70%, 50%, 0.2)`,
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 0,
    }));

    const averageDatasets: Dataset[] = Array.from({length: 16}, (_, i) => {
        const hue = (i * 22.5) % 360;  // Broader hue jumps every 22.5 degrees for 16 colors
        const saturation = 70 + (i % 2) * 10;  // Alternate between 70% and 80% for contrast
        const lightness = 50 + ((i % 3) * 10 - 10);  // Alternate between 40%, 50%, and 60%

        return {
            label: `Average Channel ${i + 1}`,
            data: Array(0).fill(100),
            borderColor: `hsl(${hue}, ${saturation}%, ${lightness}%)`,
            backgroundColor: `hsla(${hue}, ${saturation}%, ${lightness}%, 0.2)`,
            borderWidth: 3,
            tension: 0.4,
            pointRadius: 2,
            pointHoverRadius: 5,
        };
    });


    const [chartData, setChartData] = useState({
        labels: Array.from({length: 64}, (_, i) => i + 1),
        datasets: initialDatasets,
    });

    const [averageChartData, setAverageChartData] = useState({
        labels: Array.from({length: 16}, (_, i) => i + 1),
        datasets: averageDatasets,
    });

    const setNewDataValues = (values: number[]) => {
        // Update the raw data chart
        setChartData((prevData) => {
            const updatedDatasets = prevData.datasets.map((dataset, index) => {
                const updatedData = [...dataset.data, values[index]].slice(-maxDataPoints);
                return {...dataset, data: updatedData};
            });

            const updatedLabels = Array.from({length: maxDataPoints}, (_, i) => i + 1);

            return {
                ...prevData,
                labels: updatedLabels,
                datasets: updatedDatasets,
            };
        });
    }

    const setAverageChatValues = (values: number[]) => {
        const averagedValues = Array.from({length: 16}, (_, i) => {
            const indices = [i, i + 16, i + 32, i + 48];
            let sum = 0;
            let ignored_indices = indices.length;

            for (const index of indices) {
                // Values over 500kOhm are a result of a broken sensor.
                const val = values[index];
                if (val < 500000) {
                    sum += val;
                    ignored_indices -= 1;
                }
            }

            // If all indices were ignored, return 0
            if (ignored_indices === indices.length) {
                return 0;
            }
            // Median
            // const result = values[(indices.length - ignored_indices) + i] / 2;


            // Return the average for this set of indices
            return sum / (indices.length - ignored_indices);
        });

        setAverageChartData((prevAverageData) => {
            const updatedAverages = prevAverageData.datasets.map((dataset, index) => {
                const updatedData = [...dataset.data, averagedValues[index]].slice(-10);
                return {...dataset, data: updatedData};
            });

            const updatedLabels = Array.from({length: 10}, (_, i) => i + 1);

            return {
                ...prevAverageData,
                labels: updatedLabels,
                datasets: updatedAverages,
            };
        });
    }

    useEffect(() => {
        const socket = io({ path: "/socket.io" });
        setSocket(socket);

        socket.on("connect", () => {
            console.log("Connected to WebSocket");
        });

        socket.on("data_collected", (data) => {
            const testName = data['test name'];
            if (testName === test_title) {
                const new_data = data.data.toString();
                const values = new_data.split(";").map(parseFloat);
                setNewDataValues(values);
                setAverageChatValues(values);
            }
        });

        socket.on("connect_error", (error) => {
            console.error("Connection Error:", error);
        });

        socket.on("disconnect", () => {
            console.log("WebSocket connection closed");
        });

        return () => {
            socket.close();
        };
    }, []);

    return (
        <div className="grid xl:grid-cols-2 grid-cols-1 gap-4 p-4 bg-white rounded-lg shadow-md">
            <DataChart chartName={'Sensor Data - All Channels'} chartData={chartData} />
            <DataChart chartName={'Sensor Data - Averaged Channels'} chartData={averageChartData} />
        </div>
    );
};

export default RealTimeChart;
