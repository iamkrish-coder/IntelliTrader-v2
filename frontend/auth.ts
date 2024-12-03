// import NextAuth from "next-auth";
// import GoogleProvider from "next-auth/providers/google";
// import { DrizzleAdapter } from "@auth/drizzle-adapter";
// import { db } from "./lib/db";

// export const { handlers, signIn, signOut, auth } = NextAuth({
//   adapter: DrizzleAdapter(db),
//   providers: [
//     GoogleProvider({
//       clientId: process.env.GOOGLE_CLIENT_ID as string,
//       clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
//     }),
//   ],
//   pages: {
//     signIn: "/signin",
//   },
//   session: {
//     strategy: "jwt"
//   },
//   callbacks: {
//     async session({ session, user }) {
//       if (session.user) {
//         session.user.id = user.id;
//       }
//       return session;
//     },
//     async redirect({ url, baseUrl }) {
//       // Redirect to dashboard after sign in
//       if (url.startsWith(baseUrl)) return `${baseUrl}/dashboard`;
//       else if (url.startsWith("/")) return `${baseUrl}${url}`;
//       return url;
//     },
//   },
// });
