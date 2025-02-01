import { toast } from 'sonner';
import { ApiError } from '../types/api';

interface ToastOptions {
    description?: string;
    action?: {
        label: string;
        onClick: () => void;
    };
    duration?: number;
}

export const showSuccessToast = (
    message: string,
    options?: ToastOptions
) => {
    toast.success(message, {
        duration: 4000,
        ...options,
    });
};

export const showErrorToast = (
    error: Error | ApiError,
    options?: ToastOptions
) => {
    if (error instanceof ApiError) {
        // Log technical details for debugging
        console.error(error.getTechnicalDetails(), error.data);

        // Show user-friendly message
        toast.error(error.getUserMessage(), {
            duration: 5000,
            ...options,
            // Add retry action for retryable errors
            action: error.isRetryable()
                ? {
                      label: 'Retry',
                      onClick: () => window.location.reload(),
                  }
                : options?.action,
            // Add request ID for support reference
            description: options?.description || 
                `If this persists, contact support with ID: ${error.request_id}`,
        });
    } else {
        // Handle regular errors
        console.error(error);
        toast.error(error.message || 'An unexpected error occurred', {
            duration: 5000,
            ...options,
        });
    }
};

export const showLoadingToast = (
    message: string = 'Processing...',
    options?: ToastOptions
) => {
    return toast.loading(message, {
        duration: 0, // Keep until manually dismissed
        ...options,
    });
};

// Helper to dismiss a specific toast
export const dismissToast = (toastId: string) => {
    toast.dismiss(toastId);
};
