import type { Metadata } from "next";
import localFont from "next/font/local";
import { inter, montserrat, saira, dmSans, spaceGrotesk } from "@/lib/fonts";
import "./globals.css";

export const metadata: Metadata = {
  title: "IntelliTrader",
  description: "Trade Smarter Not Harder!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${montserrat.variable} ${saira.variable} ${dmSans.variable} ${spaceGrotesk.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
