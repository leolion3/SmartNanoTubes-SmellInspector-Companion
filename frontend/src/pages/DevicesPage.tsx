import React, {useEffect, useState} from "react";
import PictureWithTextCard from "../components/PictureWithTextCard";
import {Link} from "react-router-dom";
import axiosInstance from "../authentication/axios-instance";

const emptyDevice = () => {
    return {
        id: 3,
        title: 'Neues Gerät',
        mac_address: '69',
        software_version: '',
        fan_setting: '',
        serial_port: '',
        connected: 0,
        src: 'static/icons/plus.svg',
        alt: 'Weitere hinzufügen',
        maxHeight: 200,
        showStatus: false,
        link: '/add-device',
    };
}

async function fetchDevices() {
    const url = 'get_devices';
    return axiosInstance.get(url)
        .then((response: any) => {
            if (response.status !== 200) {
                return [];
            }
            return response.data;
        })
        .catch((error: any) => {
            return [];
        });
}

async function renderDevices() {
    const devices = await fetchDevices();
    const render_data = [];
    devices.forEach((device: string[5]) => {
        render_data.push({
            id: device[0],
            title: device[1],
            mac_address: device[2],
            software_version: device[3],
            fan_setting: device[4],
            serial_port: device[5],
            connected: device[6],
            src: 'static/snt-smell-inspector.webp',
            alt: 'smellinspector image',
            maxHeight: 200,
            showStatus: true,
            link: '/device-preview',
        })
    })
    render_data.push(emptyDevice());
    return render_data;
}

const DevicesPage = () => {
    const [devices, setDevices] = useState<any>([]);

    useEffect(() => {
        const fetch = async() => {
            const dev = await renderDevices();
            setDevices(dev);
        }
        fetch();
        const intervalId = setInterval(fetch, 2000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-center mb-6">Geräte Verwaltung</h1>
            <p className="text-xl font-light text-center mb-8">
                Hier können Sie die Ihnen zur Verfügung stehenden Geräte sehen und neue hinzufügen.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 mr-auto ml-auto">
                {devices.map((device: any) => (
                    <Link key={device.id} to={device.link} state={{
                        id: device.id,
                        title: device.title,
                        mac_address: device.mac_address,
                        software_version: device.software_version,
                        fan_setting: device.fan_setting,
                        serial_port: device.serial_port,
                        connected: device.connected,
                        src: device.src,
                        alt: device.alt,
                        maxHeight: 80,
                    }}>
                        <PictureWithTextCard id={device.id} src={device.src} alt="" title={device.title}
                                             description="" maxHeight={80} connected={device.connected} showStatus={device.showStatus} />
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default DevicesPage;