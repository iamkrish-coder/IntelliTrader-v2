import { auth } from "@/auth";
import Image from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { SignOutButton } from "@/components/blocks/auth/sign-out-button";

export default async function Page() {
  const session = await auth();

  if (!session?.user) {
    return null;
  }

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="text-muted-foreground">
        Welcome to your trading dashboard. Here you'll find a summary of your trading activities and performance metrics.
      </p>
      <Card>
        <CardHeader>
          <CardTitle>User Profile</CardTitle>
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
