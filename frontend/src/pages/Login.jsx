import React, { useState } from 'react';
import { useNavigate, Link } from "react-router-dom";
import { Container, Button, Card, Col, Form, Row } from "react-bootstrap";
import { toast } from 'sonner';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { loginService } from '../api';
import { LoadingSpinner } from '../components'; 
import { handleSuccess, handleError } from '../utils';

const Login = ({ assets }) => {
    // Assets
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;
    const navigate = useNavigate();

    // States
    const [showPassword, setShowPassword] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [validated, setValidated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        userEmail: '',
        userPassword: '',
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

        // Check if email is valid
        if (!isEmailValid(formData.userEmail)) {
            toast.error(MESSAGES["CLIENT_EMAIL_INVALID"]);
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
        <Container className="page-sign">
            <Card className="card-sign">
                <Card.Header>
                    <img src={ICONS.Favicon24} alt="IntelliTrader" className="header-logo mb-2 mr-2" />
                    <Link to="/" className="header-logo mb-4">IntelliTrader</Link>
                    <Card.Title>Sign In</Card.Title>
                    <Card.Text>Welcome back! Please signin to continue.</Card.Text>
                </Card.Header>
                <Card.Body>
                    <Form noValidate validated={validated} onSubmit={handleSubmit} method="post">
                        <Row className="mb-3">
                            <Form.Group md="4" controlId="userEmail">
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
                        <Row className="mb-4">
                            <Form.Group md="4" controlId="userPassword">
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
                                            {showPassword ? <FaEye /> : <FaEyeSlash /> } {/* Show/hide icon */}
                                        </span>
                                    )}
                                </div>
                            </Form.Group>
                        </Row>
                        <Button type="submit" variant="primary" className="btn-sign">
                            {loading ? <LoadingSpinner /> : 'Sign In'}
                        </Button>
                    </Form>
                </Card.Body>
                <Card.Footer>
                    Don't have an account? <Link to="/register">Create an Account</Link>
                </Card.Footer>
            </Card>
        </Container>
    )
}

export default Login