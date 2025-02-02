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
import Logo from "@/components/blocks/core/app-logo";
import Link from "next/link";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { Shell } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { toast } from "sonner";

export default function VerifyEmailRequestForm() {
  const [isLoading, setIsLoading] = useState(false);
  const searchParams = useSearchParams();
  const email = searchParams.get("email");
  const type = searchParams.get("type") || "signin"; // 'signin' or 'reset'

  const handleResendEmail = async () => {
    if (!email) {
      toast.error("Email address is required");
      return;
    }

    try {
      setIsLoading(true);
      if (type === "signin") {
        const response = await signIn("email", {
          email,
          redirect: false,
          callbackUrl: "/auth/verify",
        });
        if (response?.ok) {
          toast.success("Verification email sent successfully!");
        } else {
          toast.error("Failed to send verification email");
        }
      } else {
        // Handle password reset email resend
        const response = await fetch("/api/auth/forgot-password", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (response.ok) {
          toast.success("Password reset email sent successfully!");
        } else {
          toast.error("Failed to send password reset email");
        }
      }
    } catch (error) {
      console.error("Email resend error:", error);
      toast.error("An error occurred while sending the email");
    } finally {
      setIsLoading(false);
    }
  };

  const renderContent = () => {
    if (type === "reset") {
      return {
        title: "Check your email",
        description: "Password reset instructions sent",
        message:
          "We've sent password reset instructions to your email address:",
        buttonText: "Resend reset instructions",
      };
    }

    return {
      title: "Check your email",
      description: "Email sent to sign in to your account",
      message: "We've sent a sign in link to your email address:",
      buttonText: "Resend verification email",
    };
  };

  const content = renderContent();

  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">
          {content.title}
        </CardTitle>
        <CardDescription className="md:text-sm">
          {content.description}
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <div className="space-y-4">
          <div className="grid gap-2">
            <p className="text-sm">
              {content.message}
              <span className="font-medium"> {email} </span>
              {type === "reset"
                ? "Click the link in the email to reset your password. The link will expire in 1 hour."
                : "Click the link in the email to sign in. The link will expire in 24 hours."}
            </p>
          </div>
        </div>
        <Button
          variant="outline"
          onClick={handleResendEmail}
          disabled={isLoading}
        >
          {isLoading && <Shell className="mr-2 h-4 w-4 animate-spin" />}
          {content.buttonText}
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
