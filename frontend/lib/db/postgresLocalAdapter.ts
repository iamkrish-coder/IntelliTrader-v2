import { Adapter } from "next-auth/adapters";
import { authService } from "@/services/auth/authService";

export function PostgresLocalAdapter(): Adapter {
  return {
    async createUser(user) {
      return authService.createUser(user);
    },
    async getUser(id) {
      return authService.getUser(id);
    },
    async getUserByEmail(email) {
      return authService.getUserByEmail(email);
    },
    async getUserByAccount({ providerAccountId, provider }) {
      return authService.getUserByAccount(providerAccountId, provider);
    },
    async updateUser(user) {
      return authService.updateUser(user);
    },
    async linkAccount(account) {
      return authService.linkAccount(account);
    },
    async createSession(session) {
      return authService.createSession(session);
    },
    async getSessionAndUser(sessionToken) {
      return authService.getSessionAndUser(sessionToken);
    },
    async updateSession(session) {
      return authService.updateSession(session);
    },
    async deleteSession(sessionToken) {
      await authService.deleteSession(sessionToken);
    },
    async createVerificationToken(token) {
      return authService.createVerificationToken(token);
    },
    async useVerificationToken({ identifier, token }) {
      return authService.useVerificationToken(identifier, token);
    },
  };
} 