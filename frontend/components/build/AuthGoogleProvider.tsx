"use client";

import { AuthenticateWithGoogle } from "@/actions/oAuth";
import { Button } from "@/components/ui/button";
import { Icons } from "@/components/ui/icons";
import { notifySuccess, notifyError } from "@/lib/notification";

export default function AuthGoogleProvider() {
  const handleSignIn = async () => {
    try {
      await AuthenticateWithGoogle();
      notifySuccess("Successfully signed in with Google");
    } catch (error) {
      console.error("Error signing in with Google:", error);
      notifyError("Failed to sign in with Google");
    }
  };

  return (
    <Button variant="outline" onClick={handleSignIn}>
      <Icons.google aria-hidden className="mr-2 size-4" />
      Google
    </Button>
  );
}
