import { toast } from 'sonner';
import MESSAGES from './messages';

interface SuccessResponse {
  success?: {
    message?: string;
  };
}

interface ErrorResponse {
  error?: {
    message?: string;
    data?: string;
  };
}

export const handleSuccess = (response: SuccessResponse): void => {
  const successMessage = response?.success?.message;
  const formattedSuccessMessage = successMessage ? MESSAGES[successMessage as keyof typeof MESSAGES] || successMessage : undefined;

  if (formattedSuccessMessage) {
    toast.success(formattedSuccessMessage);
  }
};

export const handleError = (errors: ErrorResponse): void => {
  const errorMessage = errors?.error?.message;
  const errorData = errors?.error?.data;
  const formattedErrorMessage = errorMessage 
    ? MESSAGES[errorMessage as keyof typeof MESSAGES] || errorMessage 
    : MESSAGES['UNKNOWN_ERROR'];

  toast.error(formattedErrorMessage);
  if (errorData) {
    toast.error(errorData);
  }
};
