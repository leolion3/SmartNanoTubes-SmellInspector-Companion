interface IDeviceDetails {
    id: number,
    title: string;
    mac_address: string;
    software_version: string;
    fan_setting: string;
    serial_port: string;
    connected: number;
    src: string;
    alt: string;
    maxHeight: number;
}

export default IDeviceDetails;