import Image from "next/image";
import Link from "next/link";

export default function Logo() {
  return (
    <div className="flex items-center">
      <Image
        src="/vectors/logo.svg"
        alt="Brand Logo"
        width={24}
        height={24}
        className="mr-2"
        priority
      />
      <Link href="/">
        <h3 className="font-daysOne text-2xl text-gray-800 dark:text-white">
          Intell!TRADER
        </h3>
      </Link>
      <div
        className="ml-2 mt-2 h-2 w-2 animate-pulse rounded-full bg-red-600 dark:bg-white"
        aria-label="Pulsing dot"
      ></div>
    </div>
  );
}
