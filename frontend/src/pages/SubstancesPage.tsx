import React, {useEffect, useState} from "react";
import PictureWithTextCard from "../components/PictureWithTextCard";
import {Link} from "react-router-dom";
import axiosInstance from "../authentication/axios-instance";

const emptySubstance = () => {
    return {
        substance_id: '-1',
        substance_name: 'Neue Substanz Hinzufügen',
        substance_quantity: '',
        substance_description: '',
        description: '',
        src: 'static/icons/plus.svg',
        maxHeight: 200,
        showStatus: false,
        link: '/add-substance'
    };
}

async function fetchSubstances() {
    const url = 'get_substances';
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

async function renderSubstances() {
    const substances = await fetchSubstances();
    const render_data = [];
    substances.forEach((substance: any) => {
        render_data.push({
            substance_id: substance[0],
            substance_name: substance[1],
            substance_quantity: substance[2],
            substance_description: substance[1] + ' ' + substance[2],
            src: 'static/icons/vial.svg',
            maxHeight: 200,
            showStatus: true,
            link: '/substance-preview',
        })
    })
    render_data.push(emptySubstance());
    return render_data;
}

const SubstancesPage = () => {
    const [substances, setSubstances] = useState<any>([]);

    useEffect(() => {
        const fetch = async() => {
            const _substances = await renderSubstances();
            setSubstances(_substances);
        }
        fetch();
        const intervalId = setInterval(fetch, 2000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-center mb-6">Substanz Verwaltung</h1>
            <p className="text-xl font-light text-center mb-8">
                Hier können Sie Substanzen verwalten.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 mr-auto ml-auto">
                {substances.map((substance: any) => (
                    <Link key={substance.substance_id} to={substance.link} state={{
                        title: substance.substance_name + ' ' + substance.substance_quantity,
                        substance_id: substance.substance_id,
                        substance_name: substance.substance_name,
                        substance_quantity: substance.substance_quantity,
                        maxHeight: 80,
                    }}>
                        <PictureWithTextCard id={substance.substance_id} src={substance.src} alt="" title={substance.substance_name}
                                             description={substance.substance_description} maxHeight={80}
                                             connected={1} showStatus={false} />
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default SubstancesPage;