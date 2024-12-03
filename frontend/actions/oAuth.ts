"use server";

import { signIn } from "@/auth";

export async function AuthenticateWithGoogle() {
  await signIn("google", { callbackUrl: "/secure/profile" });
}

export async function AuthenticateWithGithub() {
  await signIn("github");
}
