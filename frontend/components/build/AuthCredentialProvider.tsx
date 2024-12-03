"use client";

import Link from "next/link";
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
import AuthGithubProvider from "@/components/build/AuthGithubProvider";
import AuthGoogleProvider from "@/components/build/AuthGoogleProvider";

interface AuthCredentialProviderProps {
  type: "signin" | "signup";
  title: string;
  description: string;
  action: string;
}

export default function AuthCredentialProvider({
  type,
  title,
  description,
  action,
}: AuthCredentialProviderProps) {
  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">{title}</CardTitle>
        <CardDescription className="md:text-sm">{description}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <div className="grid grid-cols-2 gap-6 md:gap-2">
          <AuthGoogleProvider />
          <AuthGithubProvider />
        </div>
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">
              Or continue with
            </span>
          </div>
        </div>
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="Enter your email address"
          />
        </div>
        <div className="grid gap-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            {type === "signin" ? (
              <Link
                href="/auth/forgot-password"
                className="text-xs text-muted-foreground hover:text-foreground hover:underline"
              >
                Forgot Password?
              </Link>
            ) : (
              ""
            )}
          </div>
          <Input
            id="password"
            type="password"
            placeholder={
              type === "signin"
                ? "Enter your password"
                : "Enter a password with at least 6 characters"
            }
          />
        </div>
      </CardContent>
      <CardFooter>
        <div className="flex w-full flex-col items-center justify-between space-y-2">
          <Button className="w-full">{action}</Button>
          {type === "signin" ? (
            <p className="mt-2 text-center text-sm">
              Don&apos;t have an account?{" "}
              <Link
                href="/auth/signup"
                className="text-muted-foreground hover:text-foreground hover:underline"
              >
                Create a new account
              </Link>
            </p>
          ) : (
            <p className="mt-2 text-center text-sm">
              Already have an account?{" "}
              <Link
                href="/auth/login"
                className="text-muted-foreground hover:text-foreground hover:underline"
              >
                Sign In
              </Link>
            </p>
          )}
        </div>
      </CardFooter>
    </Card>
  );
}
