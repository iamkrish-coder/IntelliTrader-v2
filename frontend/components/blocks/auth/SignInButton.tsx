"use client";

import { Button } from "@/components/ui/button";
import { Icons } from "@/components/ui/icons";
import { signIn } from "next-auth/react";

interface SignInButtonProps {
  provider: "google" | "microsoft";
}

export function SignInButton({ provider }: SignInButtonProps) {
  const providerConfig = {
    google: {
      text: "Sign in with Google",
      icon: <Icons.google className="h-5 w-5" />,
    },
    microsoft: {
      text: "Sign in with Microsoft",
      icon: <Icons.microsoft className="h-5 w-5" />,
    },
  };

  const config = providerConfig[provider];

  return (
    <Button
      variant="outline"
      className="flex w-full items-center justify-center gap-2"
      onClick={() => signIn(provider, { callbackUrl: "/dashboard" })}
    >
      {config.icon}
      {config.text}
    </Button>
  );
}
