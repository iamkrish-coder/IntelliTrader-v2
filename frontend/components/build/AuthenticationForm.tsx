"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Icons } from "@/components/ui/icons";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import Logo from "@/components/build/Logo";
import Link from "next/link";

interface AuthFormProps {
  type: "signin" | "signup";
  title: string;
  description: string;
  action: string;
}

export default function AuthenticationForm({
  type,
  title,
  description,
  action,
}: AuthFormProps) {
  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl md:text-xl">{title}</CardTitle>
        <CardDescription className="md:text-sm">{description}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <div className="grid grid-cols-2 gap-6 md:gap-2">
          <Button variant="outline">
            <Icons.gitHub aria-hidden className="mr-2 size-4" />
            Github
          </Button>
          <Button variant="outline">
            <Icons.google aria-hidden className="mr-2 size-4" />
            Google
          </Button>
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
          <Label htmlFor="password">Password</Label>
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
                href="/signup"
                className="text-muted-foreground hover:text-foreground hover:underline"
              >
                Create a new account
              </Link>
            </p>
          ) : (
            <p className="mt-2 text-center text-sm">
              Already have an account?{" "}
              <Link
                href="/login"
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
