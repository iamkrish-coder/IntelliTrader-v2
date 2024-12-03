'use client';

import { useSession } from "next-auth/react";
import { redirect } from "next/navigation";

export default function DashboardPage() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      redirect('/signin');
    },
  });

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2">
      <h1 className="mb-4 text-4xl font-bold">Welcome to your Dashboard</h1>
      <div className="flex items-center space-x-4">
        {session?.user?.image && (
          <img
            src={session.user.image}
            alt="Profile"
            className="h-12 w-12 rounded-full"
          />
        )}
        <div>
          <p className="text-xl font-semibold">{session?.user?.name}</p>
          <p className="text-gray-500">{session?.user?.email}</p>
        </div>
      </div>
    </div>
  );
}
