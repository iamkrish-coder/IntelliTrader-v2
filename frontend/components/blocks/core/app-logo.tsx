import Image from "next/image";
import Link from "next/link";
import { cn } from "@/lib/utils";

interface LogoProps {
  collapsed?: boolean;
  className?: string;
}

export default function Logo({ collapsed = false, className }: LogoProps) {
  return (
    <div className={cn("flex items-center", className)}>
      <Link href="/" className="flex items-center">
        <Image
          src="/vectors/logo.svg"
          alt="Brand Logo"
          width={32}
          height={32}
          className="min-w-[32px]"
          priority
        />
        <div
          className={cn(
            "ml-2 flex items-center overflow-hidden transition-all duration-300",
            collapsed ? "w-0 opacity-0" : "w-auto opacity-100",
          )}
        >
          <h3 className="whitespace-nowrap font-gugi text-2xl text-gray-800 dark:text-white">
            INTEL!iTRADER
          </h3>
          <div
            className="mx-1 mt-3 h-2 w-2 animate-pulse rounded-full bg-red-600 dark:bg-white"
            aria-label="Pulsing dot"
          ></div>
        </div>
      </Link>
    </div>
  );
}
