import React, {useEffect, useState} from "react";
import PictureWithTextCard from "../components/PictureWithTextCard";
import {Link} from "react-router-dom";
import axiosInstance from "../authentication/axios-instance";

const emptyTest = () => {
    return {
        test_name: 'Neuen Test Starten',
        description: '',
        src: 'static/icons/plus.svg',
        maxHeight: 200,
        showStatus: false,
        link: '/add-test'
    };
}

async function fetchDevices() {
    const url = 'get_active_tests';
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

async function renderTests() {
    const tests = await fetchDevices();
    const render_data = [];
    tests.forEach((test: any) => {
        render_data.push({
            test_name: test.test_name,
            device_name: test.device_nickname,
            src: 'static/icons/microscope.svg',
            maxHeight: 200,
            showStatus: true,
            link: '/test-preview',
        })
    })
    render_data.push(emptyTest());
    return render_data;
}

const TestsPage = () => {
    const [tests, setTests] = useState<any>([]);

    useEffect(() => {
        const fetch = async() => {
            const tst = await renderTests();
            setTests(tst);
        }
        fetch();
        const intervalId = setInterval(fetch, 2000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-center mb-6">Test Verwaltung</h1>
            <p className="text-xl font-light text-center mb-8">
                Hier können Sie aktive Tests verwalten.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 mr-auto ml-auto">
                {tests.map((test: any) => (
                    <Link key={test.test_name} to={test.link} state={{
                        title: test.test_name,
                        device_name: test.device_name,
                        maxHeight: 80,
                    }}>
                        <PictureWithTextCard id={test.test_name} src={test.src} alt="" title={test.test_name}
                                             description="" maxHeight={80} connected={1} showStatus={test.showStatus} />
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default TestsPage;