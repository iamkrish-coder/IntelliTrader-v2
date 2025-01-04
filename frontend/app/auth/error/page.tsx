"use client";
import ErrorCard from "@/components/auth/ErrorCard";

export default function ErrorPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <ErrorCard />
      </div>
    </div>
  );
}
