import { Inter, Montserrat,Saira, DM_Sans, Space_Grotesk } from 'next/font/google';

export const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-inter',
});

export const montserrat = Montserrat({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-montserrat',
});

export const saira = Saira({
  subsets: ['latin'],
  weight: ['400', '700'], 
  variable: '--font-saira',
});

export const dmSans = DM_Sans({
  subsets: ['latin'],
  weight: ['400', '700'], 
  variable: '--font-dm-sans',
});

export const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-space-grotesk',
});
