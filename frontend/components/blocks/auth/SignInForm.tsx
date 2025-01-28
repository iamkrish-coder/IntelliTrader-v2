"use client";

import { useState } from "react";
import Link from "next/link";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { Shell } from "lucide-react";
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
import Logo from "@/components/blocks/core/AppLogo";
import { SignInButton } from "@/components/blocks/auth/SignInButton";
import { toast } from "sonner";

export default function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleEmailAndCredentialsLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setIsLoading(true);

    if (showPassword) {
      try {
        const result = await signIn("credentials", {
          email,
          password,
          redirect: false,
          callbackUrl: "/dashboard",
        });

        if (result?.error) {
          console.log("Sign-in error:", result.error);
          toast.error("Incorrect email or password. Please try again.");
          return;
        }

        if (result?.ok) {
          toast.success("Signed in successfully!");
          router.push(result.url || "/dashboard");
        }
      } catch (error) {
        console.error("Sign-in error:", error);
        toast.error("An unexpected error occurred");
      } finally {
        setIsLoading(false);
      }
    } else {
      // Email Link Login
      try {
        const result = await signIn("email", {
          email: email,
          redirect: false,
          callbackUrl: "/auth/verify",
        });

        setIsLoading(false);

        if (result?.error) {
          console.error("Sign-in Error:", result.error);
          toast.error("Failed to send login email");
          return;
        }

        // If we get here, the email was sent successfully
        router.push(
          `/auth/verify-request?email=${encodeURIComponent(email)}&type=signin`,
        );
      } catch (error) {
        setIsLoading(false);
        console.error("Sign-in Error:", error);
        toast.error("Failed to send login email");
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

        <form onSubmit={handleEmailAndCredentialsLogin} className="grid gap-4">
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
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Shell className="mr-2 h-4 w-4 animate-spin" />
                  Sending Login Link...
                </>
              ) : (
                "Sign In with Email"
              )}
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
                  disabled={isLoading}
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Shell className="mr-2 h-4 w-4 animate-spin" />
                    Signing In...
                  </>
                ) : (
                  "Sign In with Password"
                )}
              </Button>
            </>
          )}

          <Button
            type="button"
            variant="outline"
            className="text-sm text-muted-foreground hover:text-foreground"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword
              ? "Sign In with Email instead"
              : "Sign In with Password instead"}
          </Button>
        </form>
      </CardContent>
      <CardFooter>
        <div className="flex w-full flex-col items-center justify-between space-y-2">
          <p className="text-center text-sm text-muted-foreground">
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
