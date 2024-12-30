import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { authService } from "@/services/auth/authService";
import EmailProvider from "next-auth/providers/email";
import { PostgresLocalAdapter } from '@/lib/postgresLocalAdapter';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PostgresLocalAdapter(),
  secret: process.env.NEXTAUTH_SECRET,
  providers: [
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
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials: Partial<Record<"email" | "password", unknown>>, request: Request) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }
        
        try {
          const response = await authService.login({
            email: credentials.email as string,
            password: credentials.password as string
          });
          
          if (!response) return null;

          return {
            id: response.id,
            email: credentials.email as string,
            name: response.name || credentials.email as string,
          };
        } catch (error) {
          console.error("Authentication error:", error);
          return null;
        }
      }
    }),
    EmailProvider({
      server: process.env.EMAIL_SERVER,
      from: process.env.EMAIL_FROM,
      async sendVerificationRequest({ identifier: email, url }) {
        try {
          const result = await fetch('/api/mail/send', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              to: email,
              subject: "Sign in to IntelliTrader",
              html: `
                <div style="padding: 20px; background-color: #f5f5f5;">
                  <h2>Sign in to IntelliTrader</h2>
                  <p>Click the button below to sign in to your account:</p>
                  <a 
                    href="${url}" 
                    style="
                      display: inline-block;
                      padding: 10px 20px;
                      background-color: #007bff;
                      color: white;
                      text-decoration: none;
                      border-radius: 5px;
                      margin-top: 10px;
                    "
                  >
                    Sign in
                  </a>
                  <p style="margin-top: 20px;">
                    If you didn't request this email, you can safely ignore it.
                  </p>
                </div>
              `,
            }),
          });

          if (!result.ok) {
            const error = await result.text();
            throw new Error(`Failed to send verification email: ${error}`);
          }
        } catch (error) {
          console.error('Failed to send verification email', error);
          throw new Error('Failed to send verification email');
        }
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 8 * 60 * 60, // 8 hours
  },
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
  },
  callbacks: {
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
});
