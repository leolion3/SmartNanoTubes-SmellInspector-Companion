// src/components/Navbar.tsx

import React, {useState} from 'react';
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faChartSimple, faEthernet, faMicroscope, faVial} from "@fortawesome/free-solid-svg-icons";

const Navbar: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    const headerStyles = () => {
        return "text-gray-800 hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium";
    }

    return (
        <nav className="bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <div className="flex-shrink-0">
                        <Link to="/">
                            <img src="static/logo.svg" alt="Logo" style={{height: '80px', maxHeight: '60px'}}/>
                        </Link>
                    </div>

                    {/* Menu for large screens */}
                    <div className="hidden md:flex space-x-4">
                        <Link
                            to="/"
                            className={`${headerStyles()}`}
                        >
                            <FontAwesomeIcon icon={faChartSimple} className='mr-1'/> Dashboard
                        </Link>
                        <Link to='/devices'
                              className={`${headerStyles()}`}
                        >
                            <FontAwesomeIcon icon={faEthernet} className='mr-1'/> Geräte
                        </Link>
                        <Link to='/substances'
                              className={`${headerStyles()}`}
                        >
                            <FontAwesomeIcon icon={faVial} className='mr-1'/> Substanzen
                        </Link>
                        <Link to='/tests'
                              className={`${headerStyles()}`}
                        >
                            <FontAwesomeIcon icon={faMicroscope} className='mr-1'/> Tests
                        </Link>
                    </div>

                    {/* Hamburger menu button for small screens */}
                    <div className="md:hidden">
                        <button
                            onClick={toggleMenu}
                            type="button"
                            className="text-gray-800 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400 p-2 rounded-md"
                            aria-controls="mobile-menu"
                            aria-expanded={isOpen}
                        >
                            <svg
                                className="h-6 w-6"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                {isOpen ? (
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth="2"
                                        d="M6 18L18 6M6 6l12 12"
                                    />
                                ) : (
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth="2"
                                        d="M4 6h16M4 12h16M4 18h16"
                                    />
                                )}
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* Menu for small screens */}
            {isOpen && (
                <div className="md:hidden" id="mobile-menu">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        <Link
                            to="/"
                            className="text-gray-800 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium"
                            onClick={() => setIsOpen(false)}
                        >
                            Dashboard
                        </Link>
                        <Link
                            to="/devices"
                            className="text-gray-800 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium"
                            onClick={() => setIsOpen(false)}
                        >
                            Geräte
                        </Link>
                        <Link
                            to="/substances"
                            className="text-gray-800 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium"
                            onClick={() => setIsOpen(false)}
                        >
                            Substanzen
                        </Link>
                        <Link
                            to="/tests"
                            className="text-gray-800 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium"
                            onClick={() => setIsOpen(false)}
                        >
                            Tests
                        </Link>
                    </div>
                </div>
            )}
        </nav>);
};

export default Navbar;
