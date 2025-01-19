import NextAuth from "next-auth";
import { Adapter } from "next-auth/adapters";
import Google from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import EmailProvider from "next-auth/providers/email";
import { authService } from "@/services/auth/authService";
import { PostgresLocalAdapter } from "@/lib/db/postgresLocalAdapter";
import { toast } from "sonner";
import { exit } from "process";

const adapter: Adapter = PostgresLocalAdapter();

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter,
  debug: true,
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "database",
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
        console.log('EmailProvider: Starting verification request', { email });
        
        try {      
          console.log('EmailProvider: Sending request to email API', { 
            email, 
            url,
            apiUrl: `${process.env.NEXTAUTH_URL}/api/auth/email` 
          });

          const response = await fetch(`${process.env.NEXTAUTH_URL}/api/auth/email`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
              email,
              url,
            }),
          });

          if (!response.ok) {
            const errorText = await response.text();
            console.error('EmailProvider: Failed to send email', { 
              status: response.status, 
              error: errorText 
            });
            throw new Error(`Failed to send verification email: ${errorText}`);
          }

          const result = await response.json();
          console.log('EmailProvider: Email sent successfully', result);
        } catch (error) {
          console.error('EmailProvider: Error in sendVerificationRequest:', error);
          throw error;
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
    CredentialsProvider({
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
          return null;
        }

        try {
          const response = await authService.login({
            email: credentials.email as string,
            password: credentials.password as string,
          });

          if (!response) return null;

          return {
            id: response.id,
            email: credentials.email as string,
            name: response.name || (credentials.email as string),
          };
        } catch (error) {
          console.error("Authentication error:", error);
          return null;
        }
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
      console.log('SignIn callback:', { user, account, email });
      return true;
    },
    async jwt({ token, account, profile }) {
      if (account && profile) {
        token.accessToken = account.access_token;
        token.id = profile.sub;
      }
      return token;
    },
    async session({ session, token }) {
      if (session?.user) {
        session.user.id = token.id as string;
      }
      return session;
    },
  },
  events: {
    signIn: async (message) => {
      console.log('NextAuth Event: signIn', message);
    },
    signOut: async (message) => {
      console.log('NextAuth Event: signOut', message);
    },
    createUser: async (message) => {
      console.log('NextAuth Event: createUser', message);
    },
    linkAccount: async (message) => {
      console.log('NextAuth Event: linkAccount', message);
    },
    session: async (message) => {
      console.log('NextAuth Event: session', message);
    },
  },
});
