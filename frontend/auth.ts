import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import PostgresAdapter from "@auth/pg-adapter";
import {Pool} from "pg"

const pool = new Pool({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE_NAME,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
})

export const {handlers, signIn, signOut, auth} = NextAuth({
    adapter: PostgresAdapter(pool),
    secret: process.env.AUTH_SECRET,
    session: {
        strategy: "jwt",
        maxAge: 24 * 60 * 60,
    },
    pages: {
        signIn: "/auth/signin",
    },
    providers: [
        Google({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
            allowDangerousEmailAccountLinking: true
        }),
        GitHub,
    ],
    callbacks: {
        async authorized({ auth }) {
            // Logged in users are authenticated, otherwise redirect to login page
            return !!auth
        },
        async jwt({token, user}) {
            if (user) {
                return {
                    ...token,
                    id: user.id
                };
            }
            return token;
        },
        async session({session, token}) {
            if (token) {
                return {
                    ...session,
                    user: {
                        ...session.user,
                        id: token.id as string
                    }
                }
            }
            return session;
        },
        redirect({url, baseUrl}: { url: string; baseUrl: string }) {
            // If the url is relative, prepend the baseUrl
            if (url.startsWith("/")) {
                url = `${baseUrl}${url}`;
            }
            // Allow redirects to the same origin or specified callback URLs
            if (url.startsWith(baseUrl)) {
                return url;
            }
            // Default to profile page after sign in
            return `${baseUrl}/dashboard/profile`;
        },
    },
});
