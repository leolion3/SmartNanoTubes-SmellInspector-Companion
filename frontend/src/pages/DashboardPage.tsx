import {Link} from "react-router-dom";
import PictureWithTextCard from "../components/PictureWithTextCard";
import React from "react";

const images = [
    {
        id: 1,
        title: 'Geräte Verwalten',
        description: '',
        src: 'static/snt-smell-inspector.webp',
        nav: '/devices',
    },
    {
        id: 2,
        title: 'Substanzen Verwalten',
        description: '',
        src: 'static/icons/vial.svg',
        nav: '/substances',
    },
    {
        id: 3,
        title: 'Tests Verwalten',
        description: '',
        src: 'static/icons/microscope.svg',
        nav: '/tests',
    },
];

const DashboardPage: React.FC = () => {
    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-center mb-6">Übersicht</h1>
            <p className="text-xl font-light text-center mb-8">
                Hier haben Sie eine übersicht über die Ihnen zur Verfügung stehenden Optionen
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 mr-auto ml-auto">
                {images.map((image) => (
                    <Link key={image.id} to={image.nav} replace={true}>
                        <PictureWithTextCard id={image.id} src={image.src} alt={image.title} title={image.title}
                                             description={image.description} connected={0} maxHeight={80} showStatus={false} />
                    </Link>
                ))}
            </div>
        </div>
    );
}

export default DashboardPage;