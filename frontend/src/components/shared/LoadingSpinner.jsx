// components/LoadingSpinner.jsx
import React from 'react';
import { Spinner } from 'react-bootstrap';

const LoadingSpinner = ({ size = "sm", variant = "default", message = "" }) => {
    return (
    <div className="d-flex align-items-center">
        <Spinner animation="border" size={size} variant={variant} role="status" aria-hidden="true" />
        {message && <span className="mx-2">{message}</span>}
        </div>
    );
};

export default LoadingSpinner;
