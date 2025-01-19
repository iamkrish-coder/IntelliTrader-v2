"use client";

import HeroHeaderSection from "@/components/custom/landing/HeroHeaderSection";
import HeroImageSection from "@/components/custom/landing/HeroImageSection";
import HeroFeaturesSection from "@/components/custom/landing/HeroFeaturesSection";
import HeroTechnologiesSection from "@/components/custom/landing/HeroTechnologiesSection";
import HeroFooterSection from "@/components/custom/landing/HeroFooterSection";

export default function Page() {
  return (
    <div className="min-h-screen bg-black">
      <HeroHeaderSection />
      <HeroTechnologiesSection />
      <HeroImageSection />
      <HeroFeaturesSection />
      <HeroFooterSection />
    </div>
  );
}
