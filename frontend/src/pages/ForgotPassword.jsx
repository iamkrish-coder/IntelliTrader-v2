import React, { useState } from 'react';
import { useNavigate, Link } from "react-router-dom";
import { Button, Card, Col, Container, Form, Nav, Row } from "react-bootstrap";
import { toast } from 'sonner';
import { BsGithub, BsTwitter } from "react-icons/bs";
import { forgotPasswordService } from '../api';
import { LoadingSpinner } from '../components';
import { handleSuccess, handleError } from '../utils';

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
            toast.error(MESSAGES["CLIENT_FORGOT_PASSWORD_EMAIL_REQUIRED"]);
            return;
        }

        // Check if email is valid
        if (!isEmailValid(formData.userEmail)) {
            toast.error(MESSAGES["CLIENT_EMAIL_INVALID"]);
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
        <Container className="page-auth">
            <div className="header">
                <Container>
                    <Link to="/" className="header-logo">IntelliTrader</Link>
                    <Nav className="nav-icon">
                        <Nav.Link href=""><BsTwitter /></Nav.Link>
                        <Nav.Link href=""><BsGithub /></Nav.Link>
                    </Nav>
                </Container>
            </div>
            <div className="content">
                <Container>
                    <Card className="card-auth">
                        <Card.Body className="text-center">
                            <div className="mb-5">
                                <span className="attribution">
                                    <object type="image/svg+xml" data={VECTORS.ForgotPassword} className="w-100" aria-label="svg image"></object>
                                </span>
                            </div>
                            <Card.Title>Reset your password</Card.Title>
                            <Card.Text className="mb-5">Enter your registered email address and we will send you a link to reset your password.</Card.Text>

                            <Form noValidate validated={validated} onSubmit={handleSubmit} method="post">
                                <Row className="g-2 align-items-center">
                                    <Col sm="8">
                                        <Form.Control 
                                            type="text" 
                                            placeholder="Enter email address" 
                                            name="userEmail" 
                                            value={formData.userEmail} 
                                            onChange={handleChange} 
                                            required 
                                        />
                                    </Col>
                                    <Col sm="4">
                                        <Button variant="primary" type="submit" disabled={loading}>
                                            {loading ? <LoadingSpinner /> : 'Reset'}
                                        </Button>
                                    </Col>
                                </Row>
                            </Form>
                        </Card.Body>
                    </Card>
                </Container>
            </div>
        </Container>
    )
}

export default ForgotPassword;
