"use client";

import { useSearchParams } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import Logo from "@/components/blocks/core/AppLogo";

interface ErrorCardProps {
  error?: string | null;
}

export default function ErrorCard({ error }: ErrorCardProps) {
  const getErrorMessage = (error: string) => {
    switch (error) {
      case "Configuration":
        return "There is a problem with the server configuration. Please contact support.";
      case "AccessDenied":
        return "You do not have permission to sign in.";
      case "Verification":
        return "The verification token has expired or has already been used.";
      default:
        return "An unexpected error occurred. Please try again.";
    }
  };

  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">
          Authentication Error
        </CardTitle>
        <CardDescription className="text-red-600 md:text-sm">
          Error Code: {error}
        </CardDescription>
        <CardDescription>
          {error ? getErrorMessage(error) : "An unknown error occurred"}
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <Button asChild>
          <Link href="/auth/signin">Return to Sign In</Link>
        </Button>
      </CardContent>
    </Card>
  );
}
