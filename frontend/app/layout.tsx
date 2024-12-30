import type {Metadata} from "next";
import {montserrat, spaceGrotesk, daysOne} from "@/lib/fonts";
import "./globals.css";
import {Toaster} from "sonner";
import {Providers} from "./providers";

export const metadata: Metadata = {
    title: "IntelliTrader",
    description: "Trade Smarter Not Harder!",
};

export default async function RootLayout({
                                             children,
                                         }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html
            lang="en"
            className={`${montserrat.variable} ${spaceGrotesk.variable} ${daysOne.variable}`}
        >
        <body>
        <Providers>{children}</Providers>

        <Toaster position="top-center" richColors/>
        </body>
        </html>
    );
}
