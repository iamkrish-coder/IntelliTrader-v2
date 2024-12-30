export interface OAuthUserData {
  email: string;
  name: string;
  picture: string;
  provider_id: string;
  oauth_provider: string;
}

export interface OAuthResponse {
  token?: string;
  user?: {
    id: string;
    email: string;
    name?: string;
  };
  message?: string;
}

export interface loginRequest {
  email: string;
  password: string;
}

export interface loginResponse {
  id: string;
  name?: string;
  email: string;
}
