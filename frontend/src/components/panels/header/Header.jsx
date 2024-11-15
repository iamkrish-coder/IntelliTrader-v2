// components/HeaderNav.jsx

import React, { useState, useEffect } from 'react';
import { Container, Nav } from 'react-bootstrap';

import HeaderProfile from './HeaderProfile';

const Header = () => {
    const [skin, setSkin] = useState(localStorage.getItem('skin-mode') || 'light');

    useEffect(() => {
        document.querySelector("html").setAttribute("data-skin", skin);
        localStorage.setItem("skin-mode", skin);
    }, [skin]);

    return (
        <div className="header">
            <Container>
                <HeaderProfile onSkinChange={setSkin} currentSkin={skin} />
            </Container>
        </div>
    );
};

export default Header;
