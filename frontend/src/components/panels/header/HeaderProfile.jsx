import React, { useEffect } from "react"
import { Link, useNavigate } from "react-router-dom";

import { Dropdown } from "react-bootstrap";
import { GiHamburgerMenu } from "react-icons/gi";
import { CiSearch } from "react-icons/ci";
import { RiEditLine, RiProfileLine } from "react-icons/ri";
import { MdOutlineLightMode, MdOutlineEditNote, MdOutlineManageAccounts, MdOutlineHelpOutline, MdOutlineLogout } from "react-icons/md";

import IMAGES from '../../../constants/images.js';

const HeaderProfile = ({ onSkin }) => {
    const navigate = useNavigate();

    useEffect(() => {
        const storedSkin = localStorage.getItem('skin-mode');
        if (storedSkin) {
            document.querySelector("html").setAttribute("data-skin", storedSkin);
            onSkin(storedSkin);
        }
    }, [onSkin]);

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
    }

    const toggleSkinMode = (e) => {
        e.preventDefault();
        e.target.classList.add("active");

        let node = e.target.parentNode.firstChild;
        while (node) {
            if (node !== e.target && node.nodeType === Node.ELEMENT_NODE)
                node.classList.remove("active");
            node = node.nextElementSibling || node.nextSibling;
        }

        let skin = e.target.textContent.toLowerCase();
        let HTMLTag = document.querySelector("html");

        HTMLTag.setAttribute("data-skin", skin);
        localStorage.setItem("skin-mode", skin);
        onSkin(skin);
    };

    const toggleSidebarSkin = (e) => {
        e.preventDefault();
        e.target.classList.add("active");

        let node = e.target.parentNode.firstChild;
        while (node) {
            if (node !== e.target && node.nodeType === Node.ELEMENT_NODE)
                node.classList.remove("active");
            node = node.nextElementSibling || node.nextSibling;
        }

        let skin = e.target.textContent.toLowerCase();
        let HTMLTag = document.querySelector("html");

        HTMLTag.removeAttribute("data-sidebar");

        if (skin !== "default") {
            HTMLTag.setAttribute("data-sidebar", skin);
            localStorage.setItem("sidebar-skin", skin);
        } else {
            localStorage.removeItem("sidebar-skin", skin);
        }
    };

    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('authorizationToken');
        navigate('/login');
    };

    return (
        <div className="header-main px-3 px-lg-4">
            <Link onClick={toggleSidebar} className="menu-link me-3 me-lg-4"><GiHamburgerMenu /></Link>

            <div className="form-search me-auto">
                <input type="text" className="form-control" placeholder="Search" />
                <CiSearch />
            </div>

            <Dropdown className="dropdown-skin" align="end">
                <Dropdown.Toggle as={CustomToggle}>
                    <MdOutlineLightMode />
                </Dropdown.Toggle>
                <Dropdown.Menu className="mt-10-f">
                    <label>Skin Mode</label>
                    <nav className="nav nav-skin">
                        <Link onClick={toggleSkinMode} className={localStorage.getItem("skin-mode") === "light" ? "nav-link active" : "nav-link"}>Light</Link>
                        <Link onClick={toggleSkinMode} className={localStorage.getItem("skin-mode") === "dark" ? "nav-link active" : "nav-link"}>Dark</Link>
                    </nav>
                    <hr />
                    <label>Sidebar Skin</label>
                    <nav id="toggleSidebarSkin" className="nav nav-skin">
                        <Link onClick={toggleSidebarSkin} className={!(localStorage.getItem("sidebar-skin")) ? "nav-link active" : "nav-link"}>Default</Link>
                        <Link onClick={toggleSidebarSkin} className={(localStorage.getItem("sidebar-skin") === "prime") ? "nav-link active" : "nav-link"}>Prime</Link>
                        <Link onClick={toggleSidebarSkin} className={(localStorage.getItem("sidebar-skin") === "dark") ? "nav-link active" : "nav-link"}>Dark</Link>
                    </nav>
                </Dropdown.Menu>
            </Dropdown>

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
    )
}

export default HeaderProfile;

