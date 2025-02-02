// frontend/components/blocks/landing/FeaturesSection.tsx
import { motion } from "motion/react";
import { Card } from "@/components/ui/card";
import { ChartBar, Bot, Lock, Zap } from "lucide-react";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
  },
};

const features = [
  {
    icon: <ChartBar className="mb-4 h-12 w-12 text-white" />,
    title: "Advanced Analytics",
    description: "Real-time market analysis and predictive modeling",
  },
  {
    icon: <Bot className="mb-4 h-12 w-12 text-white" />,
    title: "AI-Powered Trading",
    description: "Smart algorithms that adapt to market conditions",
  },
  {
    icon: <Lock className="mb-4 h-12 w-12 text-white" />,
    title: "Secure Platform",
    description: "Enterprise-grade security for your investments",
  },
  {
    icon: <Zap className="mb-4 h-12 w-12 text-white" />,
    title: "Lightning Fast",
    description: "Execute trades with precision and low latency",
  },
];

const HeroFeaturesSection = () => (
  <motion.div
    variants={containerVariants}
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true }}
    className="container mx-auto px-4 py-20"
  >
    <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
      {features.map((feature, index) => (
        <motion.div
          key={index}
          variants={itemVariants}
          whileHover={{ scale: 1.05 }}
          transition={{ duration: 0.2 }}
        >
          <Card className="border-gray-800 bg-gray-900 p-6 transition-all duration-300 hover:bg-gray-800">
            <div className="text-center">
              {feature.icon}
              <h3 className="mb-2 text-xl font-semibold text-white">
                {feature.title}
              </h3>
              <p className="text-gray-400">{feature.description}</p>
            </div>
          </Card>
        </motion.div>
      ))}
    </div>
  </motion.div>
);

export default HeroFeaturesSection;
