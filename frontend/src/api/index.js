import httpService from './httpService';

// Registering a user
export const registrationService = async (formData) => {
    return await httpService.post('/register', formData);
};

// logging in a user
export const loginService = async (formData) => {
    return await httpService.post('/login', formData);
};

// Forgot Password
export const forgotPasswordService = async (formData) => {
    return await httpService.post('/forgot-password', formData);
};

// Reset Password
export const resetPasswordService = async (formData) => {
    return await httpService.patch('/reset-password', formData);
};

