import IDeviceDetails from "./IDeviceDetails";


function exceptionHandler(location: any) {
    try {
        // Necessary check in case of accidental navigation
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const {
            id,
            title,
            mac_address,
            software_version,
            fan_setting,
            serial_port,
            connected,
            src,
            alt,
            maxHeight
        } = location.state as IDeviceDetails;
        return false;
    } catch (e) {
        return true;
    }
}

// TODO reload data
const getDeviceProps = (location: any) => {
    if (exceptionHandler(location)) {
        return null;
    }
    return location.state as IDeviceDetails;
}

export default getDeviceProps;