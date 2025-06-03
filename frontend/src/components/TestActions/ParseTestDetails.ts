import ITestDetails from "./ITestDetails";


function exceptionHandler(location: any) {
    try {
        // Necessary check in case of accidental navigation
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const {
            title,
            device_name,
            maxHeight
        } = location.state as ITestDetails;
        return false;
    } catch (e) {
        return true;
    }
}

// TODO reload data
const getTestDetails = (location: any) => {
    if (exceptionHandler(location)) {
        return null;
    }
    return location.state as ITestDetails;
}

export default getTestDetails;