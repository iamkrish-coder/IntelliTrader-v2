const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

const defaultHeaders = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    // Try to parse error response
    try {
      const errorData = await response.json();
      throw new Error(
        errorData.message || errorData.detail || "An error occurred",
      );
    } catch (e) {
      // If parsing fails, throw generic error with status
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }

  // Only try to parse JSON if there's content
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    return response.json();
  }

  return null;
};

const api = {
  get: async <T>(url: string): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      credentials: "include",
      headers: defaultHeaders,
    });
    return handleResponse(response);
  },

  post: async <T>(url: string, data: any): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: "POST",
      credentials: "include",
      headers: defaultHeaders,
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  patch: async <T>(url: string, data: any): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: "PATCH",
      credentials: "include",
      headers: defaultHeaders,
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  delete: async <T>(url: string): Promise<T> => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: "DELETE",
      credentials: "include",
      headers: defaultHeaders,
    });
    return handleResponse(response);
  },
};

export default api;
