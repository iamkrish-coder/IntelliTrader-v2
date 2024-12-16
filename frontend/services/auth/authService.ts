import api from "@/lib/axios";
import type { OAuthResponse, OAuthUserData } from "./types";

export const authService = {
  // Save OAuth user data to backend database
  saveOAuthUser: async (userData: OAuthUserData): Promise<OAuthResponse> => {
    const response = await api.post("/auth/create", userData);
    return response.data;
  },
};
