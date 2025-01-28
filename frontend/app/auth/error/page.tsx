"use client";

import ErrorCard from "@/components/blocks/auth/ErrorCard";
import { useSearchParams } from "next/navigation";

export default function ErrorPage() {
  const searchParams = useSearchParams();
  const error = searchParams.get("error");

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <ErrorCard error={error} />
      </div>
    </div>
  );
}
