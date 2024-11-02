// components/HeaderNav.jsx

import React from 'react';
import { Container, Nav } from 'react-bootstrap';
import { BsTwitter, BsGithub } from 'react-icons/bs';
import HeaderLogo from './HeaderLogo';

const HeaderNav = () => {
    return (
        <div className="header">
            <Container>
                <HeaderLogo />
                <Nav className="nav-icon mt-4 mb-4">
                    <Nav.Link href=""><BsTwitter /></Nav.Link>
                    <Nav.Link href=""><BsGithub /></Nav.Link>
                </Nav>
            </Container>
        </div>

    );
};

export default HeaderNav;
