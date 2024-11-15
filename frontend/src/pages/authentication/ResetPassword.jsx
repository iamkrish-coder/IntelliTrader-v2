import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useParams } from 'react-router-dom';

import { Button, Card, Col, Container, Form, Nav, Row } from "react-bootstrap";
import { toast } from 'sonner';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

import { resetPasswordService } from '../../api';
import { LoadingSpinner, BackgroundGradient, HeaderLogo } from '../../components';
import { handleSuccess, handleError } from '../../utils';

const ResetPassword = ({ assets }) => {
    // Assets
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;
    const { token } = useParams();
    const navigate = useNavigate();

    // States
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [validated, setValidated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        userPassword: '',
        userConfirmPassword: '',
    });

    useEffect(() => {
        setFormData(formData => ({
            ...formData,
            "token": token.split('=')[1]
        }));
    }, [token]);

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
        if (!validatePasswords(formData.userPassword, formData.userConfirmPassword)) {
            return;
        }

        // Handle reset password logic (e.g., API call)
        setLoading(true);
        try {
            const resetPasswordResponse = await resetPasswordService(formData);
            handleSuccess(resetPasswordResponse);
            // navigate('/login');
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
                        <Card.Title>Reset Password</Card.Title>
                        <Card.Text>Let's choose a new password for your account.</Card.Text>
                    </Card.Header>
                    <Card.Body>
                        <Form noValidate validated={validated} onSubmit={handleSubmit} method="post">
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userPassword">
                                    <Form.Label>New Password</Form.Label>
                                    <div className="password-input-container">
                                        <Form.Control
                                            type={showPassword ? "text" : "password"}
                                            placeholder="Enter your new password"
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
                                    <Form.Control.Feedback type="invalid">Please enter your new password</Form.Control.Feedback>
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userConfirmPassword">
                                    <Form.Label>Confirm New Password</Form.Label>
                                    <div className="password-input-container">
                                        <Form.Control
                                            type={showConfirmPassword ? "text" : "password"}
                                            placeholder="Confirm your new password"
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
                                    <Form.Control.Feedback type="invalid">Please confirm your new password</Form.Control.Feedback>
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="submitButton">
                                    <small>
                                    </small>
                                    <Button type="submit" variant="primary" className="btn-authentication">
                                        {loading ? <LoadingSpinner /> : 'Reset Password'}
                                    </Button>
                                </Form.Group>
                            </Row>
                        </Form>
                    </Card.Body>
                    <Card.Footer>
                        Remember your password? <Link to="/login">Back to Sign In</Link>
                    </Card.Footer>
                </Card>
            </Container>
        </React.Fragment>

    );
};

export default ResetPassword;
