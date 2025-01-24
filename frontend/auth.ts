import NextAuth from "next-auth";
import { Adapter } from "next-auth/adapters";
import Google from "next-auth/providers/google";
import EmailProvider from "next-auth/providers/email";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { PrismaClient } from "@prisma/client";
import { toast } from "sonner";

const prisma = new PrismaClient();

const adapter: Adapter = PrismaAdapter(prisma);

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter,
  debug: true,
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt",
    maxAge: 8 * 60 * 60, // 8 hours
  },
  providers: [
    EmailProvider({
      server: {
        host: process.env.EMAIL_SERVER_HOST,
        port: Number(process.env.EMAIL_SERVER_PORT),
        auth: {
          user: process.env.EMAIL_SERVER_USER,
          pass: process.env.EMAIL_SERVER_PASSWORD,
        },
      },
      from: process.env.EMAIL_FROM,
      sendVerificationRequest: async ({ identifier: email, url }) => {
        try {
          const response = await fetch(
            `${process.env.NEXTAUTH_URL}/api/auth/email`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                email,
                url,
              }),
            },
          );

          if (!response.ok) {
            const errorText = await response.text();
            console.error(`Failed to send verification email: ${errorText}`);
            return;
          }

          const result = await response.json();
          return result;
        } catch (error) {
          console.error(
            "EmailProvider: Error in sendVerificationRequest:",
            error,
          );
          return;
        }
      },
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          access_type: "offline",
          response_type: "code",
        },
      },
    }),
  ],
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
    signOut: "/auth/signin",
    verifyRequest: "/auth/verify-request",
  },
  callbacks: {
    async signIn({ user, account, email }) {
      if (account?.provider === "credentials") {
        return true;
      }
      // For OAuth and Email providers, ensure user exists in database
      return !!user;
    },
    async jwt({ token, account, profile, user }) {
      // Initial sign in
      if (account && user) {
        // Use the user ID from the database adapter
        token.id = user.id;
        token.email = user.email;
        token.name = user.name;
        if (account.provider !== "credentials") {
          token.accessToken = account.access_token;
        }
      }
      return token;
    },
    async session({ session, token }) {
      if (session?.user) {
        session.user.id = token.id as string;
        session.user.email = token.email as string;
        session.user.name = token.name as string | null;
      }
      return session;
    },
  },
  events: {
    signIn: async (message) => {
      // console.log('NextAuth Event: signIn', message);
    },
    signOut: async (message) => {
      // console.log('NextAuth Event: signOut', message);
    },
    createUser: async (message) => {
      // console.log('NextAuth Event: createUser', message);
    },
    linkAccount: async (message) => {
      // console.log('NextAuth Event: linkAccount', message);
    },
    session: async (message) => {
      // console.log('NextAuth Event: session', message);
    },
  },
});
