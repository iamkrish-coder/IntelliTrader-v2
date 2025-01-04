import { toast } from "sonner";
import MESSAGES from "./messages";

type SuccessResponse =
  | {
      success?: {
        message?: string;
      };
    }
  | string;

type ErrorResponse =
  | {
      error?: {
        message?: string;
        data?: string;
      };
    }
  | string;

export const notifySuccess = (response: SuccessResponse): void => {
  const message =
    typeof response === "string" ? response : response?.success?.message;

  const formattedSuccessMessage = message
    ? MESSAGES[message as keyof typeof MESSAGES] || message
    : undefined;

  if (formattedSuccessMessage) {
    toast.success(formattedSuccessMessage);
  }
};

export const notifyError = (response: ErrorResponse): void => {
  let errorMessage: string | undefined;
  let errorData: string | undefined;

  if (typeof response === "string") {
    errorMessage = response;
  } else {
    errorMessage = response?.error?.message;
    errorData = response?.error?.data;
  }

  const formattedErrorMessage = errorMessage
    ? MESSAGES[errorMessage as keyof typeof MESSAGES] || errorMessage
    : MESSAGES["UNKNOWN_ERROR"];

  toast.error(formattedErrorMessage);
  if (errorData) {
    toast.error(errorData);
  }
};
