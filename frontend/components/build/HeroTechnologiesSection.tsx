// frontend/components/custom/TechnologiesSection.tsx
import { motion } from "motion/react";

const technologies = [
  {
    name: "Next.js",
    logo: "https://seeklogo.com/images/N/next-js-icon-logo-EE302D5DBD-seeklogo.com.png",
    invert: false,
  },
  {
    name: "React",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1150px-React-icon.svg.png",
    invert: true,
  },
  {
    name: "Tailwind CSS",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Tailwind_CSS_Logo.svg/2048px-Tailwind_CSS_Logo.svg.png",
    invert: true,
  },
  {
    name: "Shadcn/ui",
    logo: "https://avatars.githubusercontent.com/u/139895814?s=280&v=4",
    invert: false,
  },
  {
    name: "TypeScript",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Typescript_logo_2020.svg/2048px-Typescript_logo_2020.svg.png",
    invert: false,
  },
];

interface Technology {
  logo: string;
  name: string;
  invert?: boolean;
}

const HeroTechnologiesSection = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5 }}
    className="container mx-auto px-4 py-20"
  >
    <h2 className="mb-12 text-center text-4xl font-bold text-white">
      Built With Modern Technologies
    </h2>
    <div className="grid grid-cols-2 items-center justify-items-center gap-8 md:grid-cols-5">
      {technologies.map((tech, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.1 }}
          className="flex flex-col items-center gap-4"
        >
          <div className="relative flex h-20 w-20 items-center justify-center">
            <img
              src={tech.logo}
              alt={`${tech.name} logo`}
              className={`max-h-full max-w-full object-contain ${tech.invert ? "brightness-0 invert filter" : ""}`}
            />
          </div>
          <p className="font-tech text-lg text-white">{tech.name}</p>
        </motion.div>
      ))}
    </div>
  </motion.div>
);

export default HeroTechnologiesSection;
