import NextAuth from "next-auth";
import { JWT } from "next-auth/jwt";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import { authService } from "./services/auth/authService";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      profile(profile) {
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
        };
      },
    }),
    GitHub,
  ],
  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === "google") {
        try {
          // Save user data to backend
          await authService.saveOAuthUser({
            email: user.email ?? "",
            name: user.name ?? "",
            picture: user.image ?? "",
            provider_id: account.providerAccountId ?? "",
            oauth_provider: account.provider,
          });
          return true;
        } catch (error) {
          console.error("Failed to save user data:", error);
          return false; // Prevent sign in if backend save fails
        }
      }
      return true; // Allow sign in for other providers
    },
    jwt({ token, user }: { token: JWT; user?: any }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    session({ session, token }: { session: any; token: JWT }) {
      session.user.id = token.id;
      return session;
    },
    redirect({ url, baseUrl }: { url: string; baseUrl: string }) {
      // If the url is relative, prepend the baseUrl
      if (url.startsWith("/")) {
        url = `${baseUrl}${url}`;
      }
      // Allow redirects to the same origin or specified callback URLs
      if (url.startsWith(baseUrl)) {
        return url;
      }
      // Default to profile page after sign in
      return `${baseUrl}/secure/profile`;
    },
  },
  pages: {
    signIn: "/auth/login",
    signOut: "/auth/login",
    error: "/auth/login",
  },
});
