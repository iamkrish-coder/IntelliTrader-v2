"use client";

import { Button } from "@/components/ui/button";
import { SignOutServerAction } from "@/actions/oAuthServerAction";

export function SignOutButton() {
  return (
    <Button
      variant="outline"
      onClick={() => SignOutServerAction()}
    >
      Sign Out
    </Button>
  );
}
