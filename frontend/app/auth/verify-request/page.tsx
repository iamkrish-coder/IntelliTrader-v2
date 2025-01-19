"use client";
import VerifyRequestCard from "@/components/custom/auth/VerifyRequestCard";

export default function VerifyRequestPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <VerifyRequestCard />
      </div>
    </div>
  );
}
