// src/components/Footer.tsx

import React from 'react';
import {Link} from "react-router-dom";

const Footer: React.FC = () => {
  return (
    <footer className="text-white mt-4" style={{backgroundColor: '#e4e2d6'}}>
      <div className="container mx-auto flex flex-col md:flex-row justify-center items-center px-4 space-y-4 md:space-y-0 md:space-x-8 py-8">
        {/* Map Section */}


        {/* Company Info Section */}
        <div className="w-full">
          <div className="px-4">
            <div className="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-4 gap-4 ml-4 mr-4">
              <div className="w-full ">
                <iframe
                    title="Standort"
                    className="w-full h-64 rounded-lg shadow-md"
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1424.0249122140142!2d8.215086771860477!3d53.11172057812849!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47b6df6370944f7b%3A0x9e1fcd8b538e9712!2sOldenburg%20Clinic%20AGR!5e0!3m2!1sen!2sde!4v1728056908458!5m2!1sen!2sde"
                    loading="lazy"
                ></iframe>
              </div>

              <div className='lg:ml-12 px-3 py-1' style={{backgroundColor: '#f0efe7'}}>
                <h3 className="text-black text-lg font-semibold mb-4">Adresse</h3>
                <ul className="text-black text-sm mb-4">
                  <li>
                    Klinikum Oldenburg AöR
                  </li>
                  <li>
                    Rahel-Straus-Straße 10
                  </li>
                  <li>
                    26133 Oldenburg
                  </li>
                  <br/>
                  <li>
                    Fon 0441 403-0
                  </li>
                  <li>
                    Fax 0441 403-2700
                  </li>
                  <li>
                    <a href="mailto:info@klinikum-oldenburg.de" target='_blank' rel='noreferrer' className="text-blue-500 hover:text-black">
                      info@klinikum-oldenburg.de
                    </a>
                  </li>
                  <br/>
                  <li>
                    Institutskennzeichen: 260 340 740
                  </li>
                  <li className="mt-2">
                    <img src="static/logo.svg" alt="Logo" style={{height: '80px', maxHeight: '60px'}}/>
                  </li>
                </ul>
              </div>

              <div className='lg:ml-12 px-3 py-1'>
                <h3 className="text-black text-lg font-semibold mb-4">Allgemein</h3>
                <ul className="text-black">
                  <li>
                    <a href="https://www.klinikum-oldenburg.de/zentren-kliniken" target='_blank' rel='noreferrer' className="hover:text-white">
                      Zentren & Kliniken
                    </a>
                  </li>
                  <li>
                    <a href="https://www.klinikum-oldenburg.de/medizinproduktesicherheit" target='_blank' rel='noreferrer' className="hover:text-white">
                      Medizinproduktesicherheit
                    </a>
                  </li>
                  <li>
                    <a href="https://www.klinikum-oldenburg.de/zentren-kliniken/institute-abteilungen/notfallzentrum" target='_blank' rel='noreferrer' className="hover:text-white">
                      Notfallzentrum
                    </a>
                  </li>
                  <li>
                    <a href="https://www.klinikum-oldenburg.de/besuchsregelung/aktuelle-besuchsregelung" target='_blank' rel='noreferrer' className="hover:text-white">
                      Besuchsregelung
                    </a>
                  </li>
                </ul>
              </div>

              <div className='px-3 py-1'>
                <h3 className="text-black text-lg font-semibold mb-4">Rechtliches</h3>
                <ul className="text-black">
                  <li>
                    <a href="https://www.klinikum-oldenburg.de/impressum" target='_blank' rel='noreferrer' className="hover:text-white">
                      Impressum
                    </a>
                  </li>
                  <li>
                    <a href="https://www.klinikum-oldenburg.de/datenschutz" target='_blank' rel='noreferrer' className="hover:text-white">
                      Datenschutzerklärung
                    </a>
                  </li>
                </ul>
              </div>
              <div className="sm:visible lg:hidden md:visible mr-auto ml-auto mt-4">
                <img src="static/logo.svg" alt="Logo" style={{height: '80px', maxHeight: '80px'}}/>
              </div>
            </div>

          </div>
        </div>
      </div>
        <div className="sticky bottom-0 left-0 w-full text-gray-700 text-center text-sm py-2" style={{ backgroundColor: '#dcdacf', color: '#888875' }}>
            Created by IsraTech Ltd. | Contact: <a href="mailto:support@isratech.software">support@isratech.software</a>
        </div>
    </footer>
  );
};

export default Footer;
