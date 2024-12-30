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

export default function SignUpForm() {
  return (
    <Card>
      <CardHeader className="space-y-2">
        <Logo />
        <CardTitle className="text-2xl font-bold md:text-xl">Sign Up</CardTitle>
        <CardDescription className="md:text-sm">
          It&apos;s free to signup and only takes a minute.
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 md:gap-2">
        <div className="space-y-4">
          <div className="grid gap-2">
            <Label htmlFor="name">Full Name</Label>
            <Input id="name" type="text" placeholder="Enter your full name" />
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
              placeholder="Enter a password with at least 6 characters"
            />
          </div>
          <Button className="w-full">Create Account</Button>
        </div>
      </CardContent>
      <CardFooter>
        <div className="flex w-full flex-col items-center justify-between space-y-2">
          <p className="mt-2 text-center text-sm">
            Already have an account?{" "}
            <Link
              href="/auth/signin"
              className="text-muted-foreground hover:text-foreground hover:underline"
            >
              Sign In
            </Link>
          </p>
        </div>
      </CardFooter>
    </Card>
  );
}
