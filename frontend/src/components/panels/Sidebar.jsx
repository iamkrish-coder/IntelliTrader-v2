import React, { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import { FaChevronRight, FaChevronDown } from 'react-icons/fa';

import { DashboardMenu, StrategyMenu, ConfigurationMenu } from "../../data/Menu";
import Logo from "./Logo";

const Sidebar = () => {
    const [expandedMenus, setExpandedMenus] = useState({
        dashboard: true,
        strategy: false,
        configuration: false
    });

    const populateMenu = (m) => {
        const menu = m.map((m, key) => {
            let sm;
            if (m.submenu) {
                sm = m.submenu.map((sm, key) => {
                    return (
                        <NavLink to={sm.link} className="nav-sub-link" key={key}>{sm.label}</NavLink>
                    )
                })
            }

            return (
                <li key={key} className="nav-item">
                    {(!sm) ? (
                        <NavLink to={m.link} className="nav-link">{m.icon} <span>{m.label}</span></NavLink>
                    ) : (
                        <div onClick={toggleSubMenu} className="nav-link has-sub">
                            {m.icon} <span>{m.label}</span>
                        </div>
                    )}
                    {m.submenu && <nav className="nav nav-sub">{sm}</nav>}
                </li>
            )
        });

        return (
            <ul className="nav nav-sidebar">
                {menu}
            </ul>
        );
    }

    const toggleMenu = (e, menuKey) => {
        e.preventDefault();
        setExpandedMenus(prev => ({
            ...prev,
            [menuKey]: !prev[menuKey]
        }));

        let parent = e.target.closest('.nav-group');
        parent.classList.toggle('show');
    }

    const toggleSubMenu = (e) => {
        e.preventDefault();

        let parent = e.target.closest('.nav-item');
        let node = parent.parentNode.firstChild;

        while (node) {
            if (node !== parent && node.nodeType === Node.ELEMENT_NODE)
                node.classList.remove('show');
            node = node.nextElementSibling || node.nextSibling;
        }

        parent.classList.toggle('show');
    }

    return (
        <Container fluid className="sidebar">
            <Row>
                <Col className="sidebar-header">
                    <Logo />
                </Col>
            </Row>
            <Row>
                <Col className="sidebar-body" style={{ overflowY: 'auto', maxHeight: 'calc(100vh - 100px)' }}>
                    <div className="nav-group show">
                        <div className="nav-label" onClick={(e) => toggleMenu(e, 'dashboard')}>
                            Dashboard
                            <span className="menu-icon">
                                {expandedMenus.dashboard ? <FaChevronDown /> : <FaChevronRight />}
                            </span>
                        </div>
                        {populateMenu(DashboardMenu)}
                    </div>
                    <div className="nav-group">
                        <div className="nav-label" onClick={(e) => toggleMenu(e, 'strategy')}>
                            Strategy
                            <span className="menu-icon">
                                {expandedMenus.strategy ? <FaChevronDown /> : <FaChevronRight />}
                            </span>
                        </div>
                        {populateMenu(StrategyMenu)}
                    </div>
                    <div className="nav-group">
                        <div className="nav-label" onClick={(e) => toggleMenu(e, 'configuration')}>
                            Configuration
                            <span className="menu-icon">
                                {expandedMenus.configuration ? <FaChevronDown /> : <FaChevronRight />}
                            </span>
                        </div>
                        {populateMenu(ConfigurationMenu)}
                    </div>
                </Col>
            </Row>
        </Container>
    );
}

export default Sidebar;