"use server";

import { signIn } from "@/auth";

export async function AuthenticateWithGoogle() {
  await signIn("google", { callbackUrl: "/dashboard/profile" });
}

export async function AuthenticateWithGithub() {
  await signIn("github");
}
