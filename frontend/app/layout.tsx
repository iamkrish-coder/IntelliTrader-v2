import type { Metadata } from "next";
import { montserrat, spaceGrotesk, daysOne } from "@/lib/fonts";
import "./globals.css";
import { auth } from "@/auth";
import { SessionProvider } from "next-auth/react";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "IntelliTrader",
  description: "Trade Smarter Not Harder!",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await auth();

  return (
    <html
      lang="en"
      className={`${montserrat.variable} ${spaceGrotesk.variable} ${daysOne.variable}`}
    >
      <body>
        <SessionProvider session={session}>
          {children}
          <Toaster position="top-center" richColors />
        </SessionProvider>
      </body>
    </html>
  );
}
