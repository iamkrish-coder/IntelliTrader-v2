import { toast } from 'sonner';
import MESSAGES from '../constants/messages.js';

export const handleSuccess = (response) => {
    const successMessage = response?.success?.message;
    const formattedSuccessMessage = MESSAGES[successMessage] || successMessage;

    if (formattedSuccessMessage) {
        toast.success(formattedSuccessMessage);
    }
};

export const handleError = (errors) => {
    const errorMessage = errors?.error?.message;
    const errorData = errors?.error?.data;
    const formattedErrorMessage = MESSAGES[errorMessage] || errorMessage || MESSAGES['CLIENT_UNKNOWN_ERROR'];

    toast.error(formattedErrorMessage);
    if (errorData) {
        toast.error(errorData);
    }
};