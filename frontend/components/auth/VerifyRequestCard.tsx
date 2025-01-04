"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Logo from "@/components/build/Logo";
import Link from "next/link";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { Shell } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { toast } from "sonner";

export default function VerifyRequestCard() {
  const [isLoading, setIsLoading] = useState(false);
  const searchParams = useSearchParams();
  const email = searchParams.get("email");

  const handleResendEmail = async () => {
    try {
      setIsLoading(true);
      const response = await signIn("email", {
        email: email,
        redirect: false,
      });
      if (response?.ok) {
        toast.success("Verification email sent successfully!");
      } else {
        toast.error("Failed to send verification email");
      }
    } catch (error) {
      toast.error("An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">
          Check your email
        </CardTitle>
        <CardDescription className="md:text-sm">
          Sign In link sent to your email
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <div className="space-y-4">
          <div className="grid gap-2">
            <p className="text-sm">
              We've sent a sign in link to your email address:
              <span className="font-medium"> {email} </span>
              Click the link in the email to sign in. The link will expire in 24
              hours.
            </p>
          </div>
        </div>
        <Button
          variant="outline"
          onClick={handleResendEmail}
          disabled={isLoading}
        >
          {isLoading && <Shell className="mr-2 h-4 w-4 animate-spin" />}
          Resend verification email
        </Button>
        <Button asChild>
          <Link href="/auth/signin">Return to Sign In</Link>
        </Button>
      </CardContent>
      <CardFooter>
        <div className="flex w-full flex-col items-center justify-between space-y-2">
          <p className="text-sm text-muted-foreground">
            By signing in, you agree to our{" "}
            <Link
              href="/terms"
              className="text-muted-foreground hover:text-foreground hover:underline"
            >
              Terms of Service
            </Link>{" "}
            and{" "}
            <Link
              href="/privacy"
              className="text-muted-foreground hover:text-foreground hover:underline"
            >
              Privacy Policy
            </Link>
          </p>
        </div>
      </CardFooter>
    </Card>
  );
}
