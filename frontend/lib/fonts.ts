import { Montserrat, Space_Grotesk, Days_One } from "next/font/google";

export const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-montserrat",
});

export const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-space-grotesk",
});

export const daysOne = Days_One({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-daysOne",
});
