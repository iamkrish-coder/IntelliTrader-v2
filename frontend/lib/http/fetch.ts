const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const result = async (response: Response) => {
  if (!response.ok) {
    let errorMessage = `Request failed with status code ${response.status}`;
    let errorBody;
    try {
      errorBody = await response.json();
      if (errorBody && errorBody.message) {
        errorMessage = `${errorMessage}: ${errorBody.message}`;
      }
    } catch (e) {
      // If JSON parsing fails, use the default error message
    }
    const error = new Error(errorMessage);
    (error as any).response = response;
    (error as any).body = errorBody;
    throw error;
  }
  try {
    const text = await response.text();
    return text.length > 0 ? JSON.parse(text) : null;
  } catch (e) {
    return null; // No JSON body
  }
};

const api = {
  get: async (url: string) => {
    const response = await fetch(`${API_BASE_URL}${url}`);
    return result(response);
  },

  post: async (url: string, data: any) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return result(response);
  },

  patch: async (url: string, data: any) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return result(response);
  },

  delete: async (url: string) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'DELETE',
    });
    return result(response);
  },
};

export default api;