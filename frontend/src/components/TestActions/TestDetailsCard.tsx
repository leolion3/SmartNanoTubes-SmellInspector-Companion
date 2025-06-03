/** Implements the left view of a test page split-screen */
import React, {useEffect, useRef, useState} from "react";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMicroscope} from "@fortawesome/free-solid-svg-icons";
import {Navigate, useLocation} from "react-router-dom";
import getTestDetails from "./ParseTestDetails";
import axiosInstance from "../../authentication/axios-instance";
import {serverIP} from "../../authentication/global-vars";
import {io} from 'socket.io-client';


const DeviceDetailsCard: React.FC = () => {
    const location = useLocation();
    const [substance, setSubstance] = useState<string>("air");
    const [substanceStartTime, setSubstanceStartTime] = useState<string>("00:00:00");
    const [messages, setMessages] = useState<string[]>([]);
    const [socket, setSocket] = useState<any>(null);
    const textAreaRef = useRef<HTMLTextAreaElement | null>(null);
    const data = getTestDetails(location);

    async function getCurrentSubstance() {
        const payload = {
            test_name: title
        }
        await axiosInstance.post('get_test_substance', payload)
            .then((res) => {
                if (res.status === 200) {
                    const data = res.data;
                    setSubstance(data.substance);
                    setSubstanceStartTime(data.substance_start_time);
                }
            })
            .catch(e => {
                console.log(e);
            })
    }

    useEffect(() => {
        if (textAreaRef.current) {
            textAreaRef.current.scrollTop = textAreaRef.current.scrollHeight;
        }
    }, [messages]);

    useEffect(() => {
        const socket = io('http://' + serverIP);
        setSocket(socket);
        socket.on('connect', () => {
            console.log('Connected to Flask WebSocket');
        });
        socket.on('data_collected', (data) => {
            const testName = data['test name']
            if (testName === title) {
                console.log('Message from server:', data);
                const temperature = data['temperature']
                const humidity = data['humidity']
                const measured_substance = data['substance']
                const new_data = data.data.toString();
                const stringified = 'Data: ' + new_data + ', temperature: ' + temperature + ', humidity: '
                    + humidity + ', substanz: ' + measured_substance + '\n'
                setMessages((prevMessages) => [...prevMessages, stringified]);
            }
        });
        socket.on('connect_error', (error) => {
            console.error('Connection Error:', error);
        });
        socket.on('disconnect', () => {
            console.log('WebSocket connection closed');
        });
        return () => {
            socket.close();
        };
    }, []);

    useEffect(() => {
        const fetch = async () => {
            await getCurrentSubstance();
        }
        fetch();
        const intervalId = setInterval(fetch, 2000);
        return () => clearInterval(intervalId);
    }, []);

    if (data === null) {
        return <Navigate to='/' replace/>
    }
    const {
        title,
        device_name,
        maxHeight
    } = data;
    const clearText = () => {
        setMessages([]);
    };
    return <div className="bg-gray-50 p-6 rounded-lg shadow-lg">
        <div
            className={`relative bg-white shadow-md rounded-lg overflow-hidden content-center text-center hover:bg-gray-200 transition-all duration-300`}>
            <FontAwesomeIcon icon={faMicroscope} className="mr-auto ml-auto mt-8" style={{height: `${maxHeight}px`}}/>
            <div className="p-4 mb-2">
                <h2 className="text-lg font-semibold mb-2">Test Name: {title}</h2>
                <p className={`text-gray-600`}>Aktuell gemessene Substanz: <span
                    className="font-semibold">{substance}</span></p>
                <p className={`text-gray-600`}>Start der Messung: <span
                    className="font-semibold">{substanceStartTime}</span></p>
                <p className={`text-gray-600`}>SmellInspector-Gerät: <span
                    className="font-semibold">{device_name}</span></p>
            </div>
        </div>
        <div className="relative">
            <button
                id="clear-button"
                title="Clear"
                onClick={clearText}
                className="absolute top-6 right-6 bg-gray-300 font-semibold rounded-full w-6 flex justify-center hover:bg-gray-400">
                &times;
            </button>

            <textarea
                ref={textAreaRef}
                id="data-display"
                className="form-control w-full mt-4 p-3 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent resize-none"
                rows={6}
                readOnly
                value={messages}>
            </textarea>
        </div>
    </div>
}

export default DeviceDetailsCard;