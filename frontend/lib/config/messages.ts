// messages.ts
const MESSAGES = {
    // Client Side Messages
    'UNKNOWN_ERROR': 'An unknown error occurred. Please try again or contact support.',
    'REQUIRED_INFORMATION': 'Please provide the required information.',
    'CONFIRM_PASSWORD_REQUIRED': 'Confirm password is required to complete registration.',
    'FULL_NAME_INVALID': 'Full name must contain only alphabets.',
    'FULL_NAME_REQUIRED': 'Full name is required to complete registration.',
    'EMAIL_REQUIRED': 'Email is required to complete registration.',
    'EMAIL_INVALID': 'Please provide a valid email address.',
    'PASSWORD_TOO_WEAK': 'Your password must be at least 8 characters long.',
    'PASSWORDS_DO_NOT_MATCH': 'Passwords do not match.',
    'REGISTRATION_SUCCESSFUL': 'Success! Your account has been created.',
    'REGISTRATION_FAILED': 'Failed to create account. Please try again or contact support.',
    'LOGIN_SUCCESSFUL': 'Login Successful!',
    'LOGIN_FAILED': 'Failed to login with the provided credentials. Please try again or contact support.',
    'FORGOT_PASSWORD_EMAIL_REQUIRED': 'Please enter your registered email address to reset your password.',
    'RESET_PASSWORD_FAILED': 'Failed to reset password. Please try again or contact support.',
    
    // Server Side Messages
    'INTERNAL_SERVER_ERROR': 'Oops! Something went wrong. Please try again later.',
    'USER_ID_NOT_FOUND': 'User ID not found.',
    'EMAIL_NOT_FOUND': 'Email not found.',
    'INVALID_USER_ID_EMAIL_TYPE': 'Invalid User ID or Email type.',
    'INVALID_EMAIL_FORMAT': 'Please enter a valid email address.',
    'GENERATE_JWT_FAILURE': 'Failed to generate JWT token.',
    'PASSWORD_HASH_FAILURE': 'Could not process password. Try again.',
    'SAVE_USER_DB_FAILURE': 'Error saving your account. Please try again.',
    'GET_USER_DB_FAILURE': 'Error fetching your account. Please try again.',
    'USER_ALREADY_EXISTS': 'Account already exists. Try logging in.',
    'INVALID_CREDENTIALS': 'Incorrect email or password.',
    'LOGIN_EMAIL_INCORRECT': 'Email not found. Sign up to create an account.',
    'LOGIN_PASSWORD_INCORRECT': 'Incorrect password. Please try again.',
    'FORGOT_PASSWORD_EMAIL_INCORRECT': 'We couldn\'t find an account associated with this email. Sign up to create an account.',
    'FORGOT_PASSWORD_TOKEN_GENERATION_FAILURE': 'Failed to generate forgot password token. Please try again or contact support.',
    'FORGOT_PASSWORD_EMAIL_SENDING_FAILURE': 'Failed to send forgot password email. Please try again or contact support.',
    'PASSWORD_RESET_SUCCESSFUL': 'Your password has been reset successfully.'
} as const;

export type MessageKeys = keyof typeof MESSAGES;
export default MESSAGES;
