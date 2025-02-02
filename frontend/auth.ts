import NextAuth, { DefaultSession } from "next-auth";
import { Adapter } from "next-auth/adapters";
import Google from "next-auth/providers/google";
import EmailProvider from "next-auth/providers/email";
import CredentialsProvider from "next-auth/providers/credentials";
import { PrismaAdapter } from "@auth/prisma-adapter";
import bcrypt from "bcryptjs";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const adapter: Adapter = PrismaAdapter(prisma);

// Add types for the session
declare module "next-auth" {
    interface Session {
        user: {
            id: string;
            email: string;
            name: string | null;
            linkedAccounts: string[];
        } & DefaultSession["user"];
    }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter,
  debug: true,
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt",
    maxAge: 8 * 60 * 60, // 8 hours
  },
  providers: [
    CredentialsProvider({
      id: "credentials",
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(
        credentials: Partial<Record<"email" | "password", unknown>>,
        request: Request,
      ) {
        if (!credentials?.email || !credentials?.password) {
          console.log("Missing credentials");
          return null;
        }

        try {
          const user = await prisma.user.findUnique({
            where: { email: credentials.email as string },
          });

          if (!user?.password) {
            return null;
          }

          const isValid = await bcrypt.compare(
            credentials.password as string,
            user.password,
          );

          if (!isValid) {
            return null;
          }

          return {
            id: user.id,
            email: user.email,
            name: user.name,
          };
        } catch (error) {
          console.error("Auth error:", error);
          return null;
        } finally {
          await prisma.$disconnect();
        }
      },
    }),
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
    async signIn({ user, account, profile, email }) {
      try {
        // Case 1: Credentials login - no linking needed
        if (account?.provider === "credentials") {
          return true;
        }

        // Case 2: OAuth login (e.g., Google)
        const existingUser = await prisma.user.findUnique({
          where: { email: user.email! },
          include: { accounts: true },
        });

        if (existingUser) {
          // If user exists but doesn't have this OAuth account linked
          if (!existingUser.accounts.some(acc => acc.provider === account?.provider)) {
            await prisma.account.create({
              data: {
                userId: existingUser.id,
                type: account?.type!,
                provider: account?.provider!,
                providerAccountId: account?.providerAccountId!,
                access_token: account?.access_token,
                expires_at: account?.expires_at,
                token_type: account?.token_type,
                scope: account?.scope,
                id_token: account?.id_token,
                refresh_token: account?.refresh_token,
              },
            });
          }
          return true;
        }

        // Case 3: New OAuth user - account will be created automatically by the adapter
        return true;
      } catch (error) {
        console.error("Error in signIn callback:", error);
        return false;
      } finally {
        await prisma.$disconnect();
      }
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
        // Fetch the user with their linked accounts
        const userWithAccounts = await prisma.user.findUnique({
          where: { id: token.id as string },
          include: { accounts: true },
        });

        session.user.id = token.id as string;
        session.user.email = token.email as string;
        session.user.name = token.name as string | null;
        // Add linked providers to the session
        session.user.linkedAccounts = userWithAccounts?.accounts.map(acc => acc.provider) || [];
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
