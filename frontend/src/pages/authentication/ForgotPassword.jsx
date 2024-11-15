import React, { useState } from 'react';
import { useNavigate, Link } from "react-router-dom";

import { Button, Card, Col, Container, Form, Row } from "react-bootstrap";
import { toast } from 'sonner';

import { forgotPasswordService } from '../../api';
import { LoadingSpinner, BackgroundGradient, HeaderLogo } from '../../components';
import { handleSuccess, handleError } from '../../utils';

const ForgotPassword = ({ assets }) => {
    // Assets
    const { ICONS, VECTORS, IMAGES, MESSAGES } = assets;
    const navigate = useNavigate();

    // States
    const [validated, setValidated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        userEmail: ''
    });

    // Change Handlers
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
            toast.error(MESSAGES["CLIENT_FORGOT_PASSWORD_EMAIL_REQUIRED"]);
            return;
        }

        // Validate inputs
        if (!validateEmail(formData.userEmail)) {
            return;
        }

        // Handle Forgot Password logic (e.g., API call)
        setLoading(true);
        try {
            const forgotPasswordResponse = await forgotPasswordService(formData);
            handleSuccess(forgotPasswordResponse);
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
                        <Card.Title>Forgot Password</Card.Title>
                        <Card.Text>No worries! Just type in your email and we'll send you a password reset link.</Card.Text>
                    </Card.Header>
                    <Card.Body>
                        <Form noValidate validated={validated} onSubmit={handleSubmit} method="post">
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="userEmail">
                                    <Form.Label ></Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter your registered email address"
                                        name="userEmail"
                                        value={formData.userEmail}
                                        onChange={handleChange}
                                        required
                                    />
                                </Form.Group>
                            </Row>
                            <Row className="mb-2">
                                <Form.Group md="2" controlId="submitButton">
                                    <small>
                                    </small>
                                    <Button type="submit" variant="primary" className="btn-authentication" disabled={loading}>
                                        {loading ? <LoadingSpinner /> : 'Reset'}
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
        </React.Fragment >
    )
}

export default ForgotPassword;
