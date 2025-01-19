import api from "@/lib/http/fetch";
import type {
  OAuthResponse,
  OAuthUserData,
  loginRequest,
  loginResponse,
} from "./types";
import {
  AdapterAccount,
  AdapterSession,
  AdapterUser,
  VerificationToken,
} from "next-auth/adapters";

export const authService = {
  // Save OAuth user data to backend database
  saveOAuthUser: async (userData: OAuthUserData): Promise<OAuthResponse> => {
    return api.post<OAuthResponse>("/auth/create", userData);
  },

  login: async (credentials: loginRequest): Promise<loginResponse> => {
    return api.post<loginResponse>("/auth/login", credentials);
  },

  // --- Adapter API Calls ---
  createUser: async (user: Omit<AdapterUser, "id">): Promise<AdapterUser> => {
    return api.post<AdapterUser>("/auth/users", user);
  },

  getUser: async (id: string): Promise<AdapterUser | null> => {
    return api.get<AdapterUser>(`/auth/users/${id}`);
  },

  getUserByEmail: async (email: string): Promise<AdapterUser | null> => {
    return api.get<AdapterUser>(`/auth/users/email/${email}`);
  },

  getUserByAccount: async (
    providerAccountId: string,
    provider: string,
  ): Promise<AdapterUser | null> => {
    return api.get<AdapterUser>(`/auth/users/account/${provider}/${providerAccountId}`);
  },

  updateUser: async (
    user: Partial<AdapterUser> & { id: string },
  ): Promise<AdapterUser> => {
    return api.patch<AdapterUser>(`/auth/users/${user.id}`, user);
  },

  linkAccount: async (account: AdapterAccount): Promise<AdapterAccount> => {
    return api.post<AdapterAccount>("/auth/accounts", account);
  },

  createSession: async (session: {
    sessionToken: string;
    userId: string;
    expires: Date;
  }): Promise<AdapterSession> => {
    console.log("Creating session:", session);
    return api.post<AdapterSession>("/auth/sessions", {
      sessionToken: session.sessionToken,
      userId: session.userId,
      expires: session.expires.toISOString()
    });
  },

  getSessionAndUser: async (
    sessionToken: string,
  ): Promise<{ session: AdapterSession; user: AdapterUser } | null> => {
    return api.get<{ session: AdapterSession; user: AdapterUser }>(`/auth/sessions/${sessionToken}`);
  },

  updateSession: async (
    session: Partial<AdapterSession> & { sessionToken: string },
  ): Promise<AdapterSession | null> => {
    return api.patch<AdapterSession>(`/auth/sessions/${session.sessionToken}`, session);
  },

  deleteSession: async (sessionToken: string): Promise<void> => {
    return api.delete(`/auth/sessions/${sessionToken}`);
  },

  createVerificationToken: async (
    token: VerificationToken,
  ): Promise<VerificationToken> => {
    return api.post<VerificationToken>("/auth/verification-tokens", token);
  },

  useVerificationToken: async (
    identifier: string,
    token: string,
  ): Promise<VerificationToken | null> => {
    return api.post<VerificationToken | null>("/auth/verification-tokens/use", { identifier, token });
  },
};
