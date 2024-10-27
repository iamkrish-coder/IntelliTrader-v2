import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Row, Card, Button, Form, Container } from 'react-bootstrap';
import { toast } from 'sonner';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { registrationService } from '../api';
import { LoadingSpinner } from '../components';
import { handleSuccess, handleError } from '../utils';

const Register = ({ assets }) => {
    // Assets
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;
    const navigate = useNavigate();

    // States
    const [showPassword, setShowPassword] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [validated, setValidated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        userFullName: '',
        userEmail: '',
        userPassword: '',
        userConfirmPassword: ''
    });

    // Change Handlers
    const handleFocus = () => setIsTyping(true);
    const handleBlur = () => setIsTyping(false);
    const handleMouseEnter = () => setShowPassword(true);
    const handleMouseLeave = () => setShowPassword(false);
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // Validations
    const isEmailValid = (email) => {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailPattern.test(email);
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

        // Check if full name contains only alphabets
        if (!/^[A-Za-z\s]+$/.test(formData.userFullName.trim())) {
            toast.error(MESSAGES["CLIENT_FULL_NAME_INVALID"]);
            return;
        }

        // Check if email is valid
        if (!isEmailValid(formData.userEmail)) {
            toast.error(MESSAGES["CLIENT_EMAIL_INVALID"]);
            return;
        }

        // Check if passwords match
        if (formData.userPassword !== formData.userConfirmPassword) {
            toast.error(MESSAGES["CLIENT_PASSWORDS_DO_NOT_MATCH"]);
            return;
        }

        if (formData.userPassword.length < 8) {
            toast.error(MESSAGES["CLIENT_PASSWORD_TOO_WEAK"]);
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
        <Container className="page-sign">
            <Card className="card-sign">
                <Card.Header>
                    <img src={ICONS.Favicon24} alt="IntelliTrader" className="header-logo mb-2 mr-2" />
                    <Link to="/" className="header-logo mb-4">IntelliTrader</Link>
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
                                        onFocus={handleFocus}
                                        onBlur={handleBlur}
                                        required
                                    />
                                    {isTyping && (
                                        <span
                                            onMouseEnter={handleMouseEnter}
                                            onMouseLeave={handleMouseLeave}
                                            className="password-icon"
                                        >
                                            {showPassword ? <FaEye /> : <FaEyeSlash />} {/* Show/hide icon */}
                                        </span>
                                    )}
                                </div>
                                <Form.Control.Feedback type="invalid">Please enter a password</Form.Control.Feedback>
                            </Form.Group>
                        </Row>
                        <Row className="mb-2">
                            <Form.Group md="2" controlId="userConfirmPassword">
                                <Form.Label>Confirm Password</Form.Label>
                                <Form.Control
                                    type="password"
                                    placeholder="Confirm your password"
                                    name="userConfirmPassword"
                                    value={formData.userConfirmPassword}
                                    onChange={handleChange}
                                    required
                                />
                                <Form.Control.Feedback type="invalid">Please confirm your password</Form.Control.Feedback>
                            </Form.Group>
                        </Row>
                        <Row className="mt-4 mb-2">
                            <small>By clicking <strong>Create Account</strong> below, you agree to our terms of service and privacy statement.</small>
                        </Row>
                        <Button type="submit" variant="primary" className="btn-sign">
                            {loading ? <LoadingSpinner /> : 'Create Account'}
                        </Button>
                    </Form>
                </Card.Body>
                <Card.Footer>
                    Already have an account? <Link to="/login">Sign In</Link>
                </Card.Footer>
            </Card>
        </Container>
    );
};

export default Register;
