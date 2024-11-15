import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

import { Row, Card, Button, Form, Container } from 'react-bootstrap';
import { toast } from 'sonner';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { TbRosetteDiscountCheck } from "react-icons/tb";

import { registrationService } from '../../api';
import { LoadingSpinner, BackgroundGradient, HeaderLogo } from '../../components';
import { handleSuccess, handleError } from '../../utils';

const Register = ({ assets }) => {
    // Assets
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;
    const navigate = useNavigate();

    // States
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [validated, setValidated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        userFullName: '',
        userEmail: '',
        userPassword: '',
        userConfirmPassword: ''
    });

    // Change Handlers
    const handleMouseDown = () => setShowPassword(true);
    const handleMouseUp = () => setShowPassword(false);
    const handleMouseDownConfirmPassword = () => setShowConfirmPassword(true);
    const handleMouseUpConfirmPassword = () => setShowConfirmPassword(false);
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // Validations
    const validateEmail = (email) => {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (!emailPattern.test(email)) {
            toast.error(MESSAGES["CLIENT_EMAIL_INVALID"]);
            return false;
        }
        return true;
    };

    const validateFullName = (fullName) => {
        if (!/^[A-Za-z\s]+$/.test(fullName.trim())) {
            toast.error(MESSAGES["CLIENT_FULL_NAME_INVALID"]);
            return false;
        }
        return true;
    };

    const validatePasswords = (password, confirmPassword) => {
        if (password !== confirmPassword) {
            toast.error(MESSAGES["CLIENT_PASSWORDS_DO_NOT_MATCH"]);
            return false;
        }
        if (password.length < 8) {
            toast.error(MESSAGES["CLIENT_PASSWORD_TOO_WEAK"]);
            return false;
        }
        return true;
    };

    // Submit Handler
    const handleSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();

        const form = e.currentTarget;
        setValidated(true);
        if (form.checkValidity() === false) {
            toast.error(MESSAGES["CLIENT_REQUIRED_INFORMATION"]);
            return;
        }

        // Validate inputs
        if (!validateFullName(formData.userFullName) ||
            !validateEmail(formData.userEmail) ||
            !validatePasswords(formData.userPassword, formData.userConfirmPassword)) {
            return;
        }

        // Handle registration logic (e.g., API call)
        setLoading(true);
        try {
            const registrationResponse = await registrationService(formData);
            handleSuccess(registrationResponse);
            navigate('/login');
        } catch (error) {
            handleError(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <React.Fragment>
            <BackgroundGradient />
            <Container className="authentication-container">
                <Card className="authentication-card shadow-2xl">
                    <Card.Header>
                        <HeaderLogo />
                        <Card.Title>Sign Up</Card.Title>
                        <Card.Text>It's free to signup and only takes a minute.</Card.Text>
                    </Card.Header>
                    <Card.Body>
                        <Form noValidate validated={validated} onSubmit={handleSubmit} method="post">
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userFullName">
                                    <Form.Label>Full name</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter your full name"
                                        name="userFullName"
                                        value={formData.userFullName}
                                        onChange={handleChange}
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">Please enter your full name</Form.Control.Feedback>
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userEmail">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter your email address"
                                        name="userEmail"
                                        value={formData.userEmail}
                                        onChange={handleChange}
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">Please enter a valid email address</Form.Control.Feedback>
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userPassword">
                                    <Form.Label>Password</Form.Label>
                                    <div className="password-input-container">
                                        <Form.Control
                                            type={showPassword ? "text" : "password"}
                                            placeholder="Enter your password"
                                            name="userPassword"
                                            value={formData.userPassword}
                                            onChange={handleChange}
                                            required
                                        />
                                        <span
                                            className="password-icon"
                                            onMouseDown={handleMouseDown}
                                            onMouseUp={handleMouseUp}
                                        >
                                            {showPassword ? <FaEye /> : <FaEyeSlash />} {/* Show/hide icon */}
                                        </span>
                                    </div>
                                    <Form.Control.Feedback type="invalid">Please enter a password</Form.Control.Feedback>
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userConfirmPassword">
                                    <Form.Label>Confirm Password</Form.Label>
                                    <div className="password-input-container">
                                        <Form.Control
                                            type={showConfirmPassword ? "text" : "password"}
                                            placeholder="Confirm your password"
                                            name="userConfirmPassword"
                                            value={formData.userConfirmPassword}
                                            onChange={handleChange}
                                            required
                                        />
                                        <span
                                            className="password-icon"
                                            onMouseDown={handleMouseDownConfirmPassword}
                                            onMouseUp={handleMouseUpConfirmPassword}
                                        >
                                            {showConfirmPassword ? <FaEye /> : <FaEyeSlash />} {/* Show/hide icon */}
                                        </span>
                                    </div>
                                    <Form.Control.Feedback type="invalid">Please confirm your password</Form.Control.Feedback>
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="submitButton">
                                    <div className="d-flex align-items-center">
                                        <TbRosetteDiscountCheck className="me-1" size={24} />
                                        <small className='pt-2'>By clicking <strong>Create Account</strong> below, you agree to our terms of service and privacy statement.</small>
                                    </div>
                                    <Button type="submit" variant="primary" className="btn-authentication">
                                        {loading ? <LoadingSpinner /> : 'Create Account'}
                                    </Button>
                                </Form.Group>
                            </Row>
                        </Form>
                    </Card.Body>
                    <Card.Footer>
                        Already have an account? <Link to="/login">Sign In</Link>
                    </Card.Footer>
                </Card>
            </Container>
        </React.Fragment>
    );
};

export default Register;
