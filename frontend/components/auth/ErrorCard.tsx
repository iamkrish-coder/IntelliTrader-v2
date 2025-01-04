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
import Logo from "@/components/build/Logo";

export default function ErrorCard() {
  const searchParams = useSearchParams();
  const error = searchParams.get("error");
  const errorCode = searchParams.get("code") || "Unknown Error";

  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">
          Authentication Error
        </CardTitle>
        <CardDescription className="text-red-600 md:text-sm">
          Error Code: {errorCode}
        </CardDescription>
        <CardDescription>
          {error === "Configuration"
            ? "There was a problem with the authentication configuration. Please try again later."
            : error || "An unknown error occurred"}
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
