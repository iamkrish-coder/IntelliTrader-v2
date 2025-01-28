"use server";

import { auth } from "@/auth";
import Image from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { SignOutButton } from "@/components/blocks/auth/SignOutButton";

export default async function PortfolioPage() {
  const session = await auth();

  if (!session?.user) {
    return null;
  }

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold">Portfolio</h1>
      <p className="text-muted-foreground">
        View and manage your current portfolio holdings and performance metrics.
      </p>
      <Card>
        <CardHeader>
          <CardTitle>Portfolio</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-4">
            {session.user.image && (
              <Image
                src={session.user.image}
                alt={session.user.name || "Portfolio"}
                width={96}
                height={96}
                className="rounded-full"
              />
            )}
            <div>
              <h2 className="text-2xl font-bold">{session.user.name}</h2>
              <p className="text-gray-500">{session.user.email}</p>
            </div>
          </div>
          <div className="mt-6">
            <SignOutButton />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
