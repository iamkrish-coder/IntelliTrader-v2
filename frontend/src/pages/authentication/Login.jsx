import React, { useState } from 'react';
import { useNavigate, Link } from "react-router-dom";
import { Container, Button, Card, Col, Form, Row } from "react-bootstrap";
import { toast } from 'sonner';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { loginService } from '../../api';
import { LoadingSpinner, BackgroundGradient, HeaderLogo, HeaderNav } from '../../components';
import { handleSuccess, handleError } from '../../utils';

const Login = ({ assets }) => {
    // Assets
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;
    const navigate = useNavigate();

    // States
    const [showPassword, setShowPassword] = useState(false);
    const [validated, setValidated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        userEmail: '',
        userPassword: '',
    });

    // Change Handlers
    const handleMouseDown = () => setShowPassword(true);
    const handleMouseUp = () => setShowPassword(false);
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
        if (!validateEmail(formData.userEmail)) {
            return;
        }

        // Handle sign in logic (e.g., API call)
        setLoading(true);
        try {
            const loginResponse = await loginService(formData);
            handleSuccess(loginResponse);
            // navigate('/home');
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
                        <Card.Title>Sign In</Card.Title>
                        <Card.Text>Welcome back! Please sign-in to continue.</Card.Text>
                    </Card.Header>
                    <Card.Body>
                        <Form noValidate validated={validated} onSubmit={handleSubmit} method="post">
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userEmail">
                                    <Form.Label >Email address</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter your email address"
                                        name="userEmail"
                                        value={formData.userEmail}
                                        onChange={handleChange}
                                        required
                                    />
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userPassword">
                                    <Form.Label className="d-flex justify-content-between">Password
                                        <Link to="/forgot-password">Forgot password?</Link>
                                    </Form.Label>
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
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="submitButton">
                                    <small>
                                    </small>
                                    <Button type="submit" variant="primary" className="btn-authentication">
                                        {loading ? <LoadingSpinner /> : 'Sign In'}
                                    </Button>
                                </Form.Group>
                            </Row>
                        </Form>
                    </Card.Body>
                    <Card.Footer>
                        Don't have an account? <Link to="/register">Create an Account</Link>
                    </Card.Footer>
                </Card>
            </Container>
        </React.Fragment>
    )
}

export default Login