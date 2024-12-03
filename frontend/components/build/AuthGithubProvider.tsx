"use client";

import { AuthenticateWithGithub } from "@/actions/oAuth";
import { Button } from "@/components/ui/button";
import { Icons } from "@/components/ui/icons";
import { toast } from "sonner";

export default function AuthGithubProvider() {
  const handleSignIn = async () => {
    try {
      await AuthenticateWithGithub();
    } catch (error) {
      console.error("Error signing in with GitHub:", error);
      toast.error("Failed to sign in with GitHub");
    }
  };

  return (
    <Button variant="outline" onClick={handleSignIn}>
      <Icons.gitHub aria-hidden className="mr-2 size-4" />
      Github
    </Button>
  );
}
