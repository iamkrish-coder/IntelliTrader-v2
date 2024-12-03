import Image from "next/image";
import Link from "next/link";

export default function Logo() {
  return (
    <div className="flex items-center">
      <Image
        src="/vectors/logo.svg"
        alt="Brand Logo"
        width={32}
        height={32}
        className="mr-2"
      />
      <Link href="/">
        <h3 className="font-dmSans text-4xl text-black dark:text-white">
          IntelliTrader
        </h3>
      </Link>
      <div
        className="ml-2 mt-4 h-2 w-2 animate-pulse rounded-full bg-red-600 dark:bg-white"
        aria-label="Pulsing dot"
      ></div>
    </div>
  );
}
