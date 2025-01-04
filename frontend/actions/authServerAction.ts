"use server";

import { signIn, signOut } from "@/auth";

export async function SignInWithGoogleServerAction() {
  await signIn("google", { callbackUrl: "/dashboard/profile" });
}

export async function SignInWithGitHubServerAction() {
  await signIn("github");
}

export async function SignOutServerAction() {
  await signOut({ redirect: true, redirectTo: "/auth/signin" });
}
