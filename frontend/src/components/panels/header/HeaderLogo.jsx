// components/HeaderLogo.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import ICONS from '../../../constants/icons.js';

const HeaderLogo = () => {

    return (
        <Container className="header-logo-container">
            <img src={ICONS.Favicon24} alt="IntelliTrader Logo" />
            <Link to="/" className="header-logo-text ml-2 flex items-center">IntelliTrader</Link>
            <span className="relative flex h-2 w-2 ml-2 mt-2 align-self-center">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-70"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-sky-500"></span>
            </span>
        </Container>
    );
};

export default HeaderLogo;
