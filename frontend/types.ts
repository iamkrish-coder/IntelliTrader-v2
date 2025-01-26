import { DefaultSession } from "next-auth";

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