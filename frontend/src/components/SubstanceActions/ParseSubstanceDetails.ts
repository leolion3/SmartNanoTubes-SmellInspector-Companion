import ISubstanceDetails from "./ISubstanceDetails";


function exceptionHandler(location: any) {
    try {
        // Necessary check in case of accidental navigation
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const {
            title,
            substance_id,
            substance_name,
            substance_quantity,
            maxHeight
        } = location.state as ISubstanceDetails;
        return false;
    } catch (e) {
        return true;
    }
}

// TODO reload data
const getSubstanceDetails = (location: any) => {
    if (exceptionHandler(location)) {
        return null;
    }
    return location.state as ISubstanceDetails;
}

export default getSubstanceDetails;