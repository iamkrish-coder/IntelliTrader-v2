// components/HeaderNav.jsx

import React, { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom";
import { Container, Dropdown } from "react-bootstrap";
import { CgMenuGridO, CgMenuGridR } from "react-icons/cg";
import { CiSearch } from "react-icons/ci";
import { RiProfileLine } from "react-icons/ri";
import { MdOutlineHelpOutline, MdOutlineManageAccounts, MdOutlineLogout } from "react-icons/md";

import Logo from './Logo.jsx';
import IMAGES from '../../constants/images.js';

const Header = () => {
    const navigate = useNavigate();
    const [isSidebarVisible, setIsSidebarVisible] = useState(true);

    const CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
        <Link to="" ref={ref} className="dropdown-link" onClick={(e) => {
            e.preventDefault();
            onClick(e);
        }}>
            {children}
        </Link>
    ));

    const toggleSidebar = (e) => {
        e.preventDefault();
        setIsSidebarVisible(prev => !prev);

        let isOffset = document.body.classList.contains("sidebar-offset");
        if (isOffset) {
            document.body.classList.toggle("sidebar-show");
        } else {
            if (window.matchMedia("(max-width: 991px)").matches) {
                document.body.classList.toggle("sidebar-show");
            } else {
                document.body.classList.toggle("sidebar-hide");
            }
        }
    };

    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('authorizationToken');
        navigate('/login');
    };

    return (
        <Container className="header">
            <div className="header-main d-flex justify-content-between align-items-center px-3 px-lg-4">
                <Link onClick={toggleSidebar} className="menu-link me-3 me-lg-4">
                    {isSidebarVisible ? <CgMenuGridO /> : <CgMenuGridR />}
                </Link>

                {!isSidebarVisible && <Logo />}

                <div className="form-search ms-auto me-3">
                    <input type="text" className="form-control" placeholder="Search" />
                    <CiSearch />
                </div>

                <div className="d-flex align-items-center">
                    <Dropdown className="dropdown-profile ms-3 ms-xl-4" align="end">
                        <Dropdown.Toggle as={CustomToggle}>
                            <div className="avatar online">
                                <img src={IMAGES.Avatar1} alt="" />
                            </div>
                        </Dropdown.Toggle>
                        <Dropdown.Menu className="mt-10-f">
                            <div className="dropdown-menu-body">
                                <div className="avatar avatar-xl online mb-3"><img src={IMAGES.Avatar1} alt="" /></div>
                                <h5 className="mb-1 text-dark fw-semibold">Srikrishnan P</h5>
                                <p className="fs-sm text-secondary">IntelliTrader User</p>

                                <nav className="nav">
                                    <Link to=""><RiProfileLine className="mr-2" /> View Profile</Link>
                                </nav>
                                <hr />
                                <nav className="nav">
                                    <Link to=""><MdOutlineHelpOutline className="mr-2" /> Help Center</Link>
                                    <Link to=""><MdOutlineManageAccounts className="mr-2" /> Account Settings</Link>
                                    <Link to="" onClick={handleLogout}><MdOutlineLogout className="mr-2" /> Log Out</Link>
                                </nav>
                            </div>
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
            </div>
        </Container>
    );
};

export default Header;
