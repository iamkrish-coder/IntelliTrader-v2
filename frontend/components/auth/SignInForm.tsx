"use client";

import { useState } from "react";
import Link from "next/link";
import { signIn } from "next-auth/react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import Logo from "@/components/build/Logo";
import { SignInButton } from "@/components/auth/SignInButton";
import { useRouter } from "next/router";

export default function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleCredentialsLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    if (showPassword) {
      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        // Handle error
        return;
      }
      // Handle success
    } else {
      try {
        const response = await fetch("/api/auth/email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (!response.ok) throw new Error("Failed to send email");

        // Redirect to verify-request page
        router.push("/auth/verify-request");
      } catch (error) {
        console.error("Error sending magic link:", error);
        // Show error toast
      }
    }
  };

  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">Sign In</CardTitle>
        <CardDescription className="md:text-sm">
          Welcome back! Please sign in to your account.
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <div className="grid gap-2">
          <SignInButton provider="google" />
          <SignInButton provider="microsoft" />
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">Or</span>
          </div>
        </div>

        <form onSubmit={handleCredentialsLogin} className="grid gap-4">
          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email address"
              required
            />
          </div>

          {!showPassword && (
            <Button type="submit" className="w-full">
              Sign in with Email
            </Button>
          )}

          {showPassword && (
            <>
              <div className="grid gap-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Password</Label>
                  <Link
                    href="/auth/forgot-password"
                    className="text-xs text-muted-foreground hover:text-foreground hover:underline"
                  >
                    Forgot Password?
                  </Link>
                </div>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                />
              </div>
              <Button type="submit" className="w-full">
                Sign In with Password
              </Button>
            </>
          )}

          <Button
            type="button"
            variant="ghost"
            className="text-sm text-muted-foreground hover:text-foreground"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword
              ? "Sign in with email instead"
              : "Sign in with password instead"}
          </Button>
        </form>
      </CardContent>
      <CardFooter>
        <div className="flex w-full flex-col items-center justify-between space-y-2">
          <p className="mt-2 text-center text-sm">
            Don&apos;t have an account?{" "}
            <Link
              href="/auth/signup"
              className="text-muted-foreground hover:text-foreground hover:underline"
            >
              Create a new account
            </Link>
          </p>
        </div>
      </CardFooter>
    </Card>
  );
}
