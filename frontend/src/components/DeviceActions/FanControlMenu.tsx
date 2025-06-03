import React from "react";


const FanControlMenu: React.FC = () => {
    return (<div className="bg-white p-6 rounded-lg shadow-lg">
        <p className='ml-auto mr-auto mb-2 mt-0 font-medium text-gray-900'>
            Aktives Lüfter Profil
        </p>
        <button
            className="px-4 py-2 bg-blue-500 text-white rounded-l-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
            Button 1
        </button>
        <button
            className="px-4 py-2 bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
            Button 2
        </button>
        <button
            className="px-4 py-2 bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
            Button 2
        </button>
        <button
            className="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
            Button 3
        </button>
    </div>);
}

export default FanControlMenu;