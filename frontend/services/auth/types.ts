export interface AuthResponse {
  token?: string;
  user?: {
    id: string;
    email: string;
    name?: string;
  };
  message?: string;
}
