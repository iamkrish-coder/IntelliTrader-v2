// frontend/components/custom/CTASection.tsx
import { motion } from "motion/react";
import { Button } from "@/components/ui/button";

const HeroFooterSection = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5 }}
    className="container mx-auto px-4 py-20 text-center"
  >
    <h2 className="mb-8 text-4xl font-bold text-white">
      Ready to Transform Your Trading?
    </h2>
    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
      <Button
        size="lg"
        className="rounded-full bg-white px-8  py-6 text-lg text-black hover:bg-gray-200"
      >
        Start Trading Now
      </Button>
    </motion.div>
  </motion.div>
);

export default HeroFooterSection;
