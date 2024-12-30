import api from "@/lib/fetch";
import type { OAuthResponse, OAuthUserData, loginRequest, loginResponse } from "./types";
import { AdapterAccount, AdapterSession, AdapterUser, VerificationToken } from "next-auth/adapters";

export const authService = {
  // Save OAuth user data to backend database
  saveOAuthUser: async (userData: OAuthUserData): Promise<OAuthResponse> => {
    return api.post("/auth/create", userData);
  },
  
  login: async (credentials: loginRequest): Promise<loginResponse> => {
    return api.post("/auth/login", credentials);
  },

  // --- Adapter API Calls ---
  createUser: async (user: Omit<AdapterUser, "id">): Promise<AdapterUser> => {
    return api.post("/auth/users", user);
  },

  getUser: async (id: string): Promise<AdapterUser | null> => {
    return api.get(`/auth/users/${id}`);
  },

  getUserByEmail: async (email: string): Promise<AdapterUser | null> => {
    return api.get(`/auth/users/email/${email}`);
  },

  getUserByAccount: async (providerAccountId: string, provider: string): Promise<AdapterUser | null> => {
    return api.get(`/auth/users/account?provider=${provider}&providerAccountId=${providerAccountId}`);
  },

  updateUser: async (user: Partial<AdapterUser> & { id: string }): Promise<AdapterUser> => {
    return api.patch(`/auth/users/${user.id}`, user);
  },

  linkAccount: async (account: AdapterAccount): Promise<AdapterAccount> => {
    return api.post("/auth/accounts", account);
  },

  createSession: async (session: { userId: string; expires: Date; sessionToken: string }): Promise<AdapterSession> => {
    return api.post("/auth/sessions", session);
  },

  getSessionAndUser: async (sessionToken: string): Promise<{ session: AdapterSession; user: AdapterUser } | null> => {
    return api.get(`/auth/sessions/${sessionToken}`);
  },

  updateSession: async (session: Partial<AdapterSession> & { sessionToken: string }): Promise<AdapterSession | null> => {
    return api.patch(`/auth/sessions/${session.sessionToken}`, session);
  },

  deleteSession: async (sessionToken: string): Promise<void> => {
    return api.delete(`/auth/sessions/${sessionToken}`);
  },

  createVerificationToken: async (token: VerificationToken): Promise<VerificationToken> => {
    return api.post("/auth/verification-tokens", token);
  },

  useVerificationToken: async (identifier: string, token: string): Promise<VerificationToken | null> => {
    return api.post("/auth/verification-tokens/use", { identifier, token });
  },
};
