import api from '@/lib/axios';
import type { 
  LoginCredentials, 
  RegistrationData, 
  ForgotPasswordData, 
  ResetPasswordData,
  AuthResponse 
} from './types';

export const authService = {
  // Register a new user
  register: async (data: RegistrationData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  // Login user
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  // Forgot password
  forgotPassword: async (data: ForgotPasswordData): Promise<{ message: string }> => {
    const response = await api.post('/auth/forgot-password', data);
    return response.data;
  },

  // Reset password
  resetPassword: async (data: ResetPasswordData): Promise<{ message: string }> => {
    const response = await api.patch('/auth/reset-password', data);
    return response.data;
  },

  // Save OAuth user data
  saveOAuthUser: async (userData: any): Promise<AuthResponse> => {
    const response = await api.post('/auth/oauth/save', userData);
    return response.data;
  }
};
