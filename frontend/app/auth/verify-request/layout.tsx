import { Metadata } from "next";
import { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Verify Email",
  description: "Verify your email address to continue",
};

export default function VerifyRequestLayout({
  children,
}: {
  children: ReactNode;
}) {
  return children;
}
