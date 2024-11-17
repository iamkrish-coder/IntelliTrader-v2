// pages/NotFound.jsx
import React from 'react';
import { Col, Container, Nav, Row } from "react-bootstrap";
import { Link } from "react-router-dom";

import { LoadingSpinner, BackgroundGradient, Logo } from '../../components';


function PageNotFound({ assets }) {
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;

    return (
        <React.Fragment>
            <object type="image/svg+xml" data={VECTORS.ErrorPage} className="error-svg" aria-label="svg image"></object>
            <Container className="page-error">
                <Logo />
                <div className="content">
                    <h1 className="error-number">404</h1>
                    <h2 className="error-title">Page Not Found</h2>
                    <p className="error-text">Sorry, the page you are looking for does not exist.</p>
                    <Link to="/dashboard/overview" className="btn btn-warning">Back to Dashboard</Link>
                </div>
            </Container>
        </React.Fragment>
    );
}

export default PageNotFound;
