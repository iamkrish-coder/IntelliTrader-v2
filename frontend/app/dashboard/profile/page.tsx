"use client";

import { useSession, signOut } from "next-auth/react";
import { redirect } from "next/navigation";
import Image from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function Page() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      redirect("/auth/signin");
    },
  });

  if (status === "loading") {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-12 w-12 animate-spin rounded-full border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mx-auto max-w-5xl space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-6">
              <div className="relative h-24 w-24 flex-shrink-0">
                {session?.user?.image ? (
                  <Image
                    src={session.user.image}
                    alt={session.user.name || "Profile picture"}
                    className="rounded-full object-cover"
                    fill
                    sizes="(max-width: 96px) 100vw, 96px"
                    priority
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center rounded-full bg-gray-200">
                    <span className="text-2xl font-medium text-gray-600">
                      {session?.user?.name?.charAt(0) || "U"}
                    </span>
                  </div>
                )}
              </div>
              <div className="flex flex-col space-y-1">
                <h3 className="text-xl font-bold text-gray-900">
                  {session?.user?.name || "User"}
                </h3>
                <p className="text-sm text-gray-500">{session?.user?.email}</p>
                <Button
                  variant="outline"
                  className="mt-2"
                  onClick={() => signOut({ callbackUrl: "/auth/signin" })}
                >
                  Sign Out
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Portfolio Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Your portfolio details will appear here
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Trades</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Your recent trading activity will appear here
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Market Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Market statistics will appear here
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
