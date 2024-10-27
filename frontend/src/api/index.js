import _API_ from './proxy';

// Registering a user
export const registrationService = async (formData) => {
    return await _API_.post('/register', formData);
};

// logging in a user
export const loginService = async (formData) => {
    return await _API_.post('/login', formData);
};

// Forgot Password
export const forgotPasswordService = async (formData) => {
    return await _API_.post('/forgot-password', formData);
};

