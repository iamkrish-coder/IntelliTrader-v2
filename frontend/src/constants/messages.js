// messages.js
const MESSAGES = {
    // Client Side Messages
    'CLIENT_UNKNOWN_ERROR': 'An unknown error occurred. Please try again or contact support.',
    'CLIENT_REQUIRED_INFORMATION': 'Please provide the required information.',
    'CLIENT_CONFIRM_PASSWORD_REQUIRED': 'Confirm password is required to complete registration.',
    'CLIENT_FULL_NAME_INVALID': 'Full name must contain only alphabets.',
    'CLIENT_FULL_NAME_REQUIRED': 'Full name is required to complete registration.',
    'CLIENT_EMAIL_REQUIRED': 'Email is required to complete registration.',
    'CLIENT_EMAIL_INVALID': 'Please provide a valid email address.',
    'CLIENT_PASSWORD_TOO_WEAK': 'Your password must be at least 8 characters long.',
    'CLIENT_PASSWORDS_DO_NOT_MATCH': 'Passwords do not match.',
    'CLIENT_REGISTRATION_SUCCESSFUL': 'Success! Your account has been created.',
    'CLIENT_REGISTRATION_FAILED': 'Failed to create account. Please try again or contact support.',
    'CLIENT_LOGIN_SUCCESSFUL': 'Login Successful!',
    'CLIENT_LOGIN_FAILED': 'Failed to login with the provided credentials. Please try again or contact support.',
    'CLIENT_FORGOT_PASSWORD_EMAIL_REQUIRED': 'Please enter your registered email address to reset your password.',
    'CLIENT_RESET_PASSWORD_FAILED': 'Failed to reset password. Please try again or contact support.',
    
    // Server Side Messages
    'SERVER_INTERNAL_SERVER_ERROR': 'Oops! Something went wrong. Please try again later.',
    'SERVER_REQUIRED_INFORMATION': 'Please provide the required information.',
    'SERVER_USER_ID_NOT_FOUND': 'User ID not found.',
    'SERVER_EMAIL_NOT_FOUND': 'Email not found.',
    'SERVER_INVALID_USER_ID_EMAIL_TYPE': 'Invalid User ID or Email type.',
    'SERVER_INVALID_EMAIL_FORMAT': 'Please enter a valid email address.',
    'SERVER_JWT_GENERATION_FAILED': 'Failed to generate JWT token.',
    'SERVER_PASSWORD_HASH_FAILURE': 'Could not process password. Try again.',
    'SERVER_SAVE_USER_DB_FAILURE': 'Error saving your account. Please try again.',
    'SERVER_GET_USER_DB_FAILURE': 'Error fetching your account. Please try again.',
    'SERVER_USER_ALREADY_EXISTS': 'Account already exists. Try logging in.',
    'SERVER_REGISTRATION_SUCCESSFUL': 'Success! Your account has been created.',
    'SERVER_REGISTRATION_FAILED': 'Could not create account. Try again or contact support.',
    'SERVER_INVALID_CREDENTIALS': 'Incorrect email or password.',
    'SERVER_LOGIN_EMAIL_INCORRECT': 'Email not found. Sign up to create an account.',
    'SERVER_LOGIN_PASSWORD_INCORRECT': 'Incorrect password. Please try again.',
    'SERVER_LOGIN_FAILED': 'An unknown error occurred. Please try again or contact support.',
    'SERVER_LOGIN_SUCCESSFUL': 'Welcome back! You have successfully logged in.',
    'SERVER_FORGOT_PASSWORD_EMAIL_INCORRECT': 'We couldn\'t find an account associated with this email. Sign up to create an account.',
    'SERVER_FORGOT_PASSWORD_TOKEN_GENERATION_FAILURE': 'Failed to generate forgot password token. Please try again or contact support.',
    'SERVER_FORGOT_PASSWORD_EMAIL_SENDING_FAILURE': 'Failed to send forgot password email. Please try again or contact support.',
    'SERVER_FORGOT_PASSWORD_EMAIL_SENT': 'We\'ve sent you an email with a link to reset your password.',
    'SERVER_FORGOT_PASSWORD_TOKEN_SAVING_FAILURE': 'Failed to save forgot password token. Please try again or contact support.'
};

export default MESSAGES;
