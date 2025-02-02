import {
  ApiSuccessResponse,
  ApiErrorResponse,
  ApiError,
  isApiErrorResponse,
  isApiSuccessResponse,
} from "../types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

const defaultHeaders = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

async function handleResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type");
  if (!contentType?.includes("application/json")) {
    throw new ApiError(
      "Invalid response format from server",
      "network-error",
      response.url,
      response.type,
      null,
      response.status,
    );
  }

  const jsonResponse = await response.json();

  // Check for API error response
  if (isApiErrorResponse(jsonResponse)) {
    throw new ApiError(
      jsonResponse.error.message,
      jsonResponse.error.request_id,
      jsonResponse.error.path,
      jsonResponse.error.method,
      jsonResponse.error.data,
      response.status,
    );
  }

  // Validate success response
  if (!isApiSuccessResponse<T>(jsonResponse)) {
    throw new ApiError(
      "Invalid response format from server",
      "format-error",
      response.url,
      response.type,
      jsonResponse,
      response.status,
    );
  }

  return jsonResponse.data;
}

async function makeRequest<T>(url: string, options: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      credentials: "include",
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    return await handleResponse<T>(response);
  } catch (error) {
    // Handle network errors
    if (error instanceof TypeError && error.message === "Failed to fetch") {
      throw new ApiError(
        "Unable to connect to server. Please check your internet connection.",
        "network-error",
        url,
        options.method || "GET",
        null,
        0,
      );
    }
    throw error;
  }
}

const api = {
  get: async <T>(url: string): Promise<T> => {
    return makeRequest<T>(url, {
      method: "GET",
    });
  },

  post: async <T>(url: string, data: any): Promise<T> => {
    return makeRequest<T>(url, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  patch: async <T>(url: string, data: any): Promise<T> => {
    return makeRequest<T>(url, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  delete: async <T>(url: string): Promise<T> => {
    return makeRequest<T>(url, {
      method: "DELETE",
    });
  },
};

export default api;
