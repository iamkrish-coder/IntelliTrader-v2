import { motion } from "motion/react";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";

export const HeroHeaderSection = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="container mx-auto flex justify-center px-4 pb-32 pt-20"
    >
      <div className="text-center">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="flex justify-center"
        >
          <Image
            src="/vectors/Logo.svg"
            alt="IntelliTrader Logo"
            width={128}
            height={128}
            className="mb-4 invert-0 filter"
          />
        </motion.div>
        <motion.h1
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-2 bg-clip-text font-saira text-8xl font-extrabold tracking-tight text-white md:text-8xl"
        >
          IntelliTrader
        </motion.h1>
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="mb-4 mt-4 pb-8 pt-4 font-montserrat text-2xl font-light text-gray-300 md:text-3xl"
        >
          "Unleash the Power of Trading with Intelligence"
        </motion.p>
        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          <Link href="/login">
            <Button
              size="lg"
              className="rounded-full bg-white text-lg text-black hover:bg-gray-200"
            >
              Get Started
            </Button>
          </Link>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default HeroHeaderSection;
