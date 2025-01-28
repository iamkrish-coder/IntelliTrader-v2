"use client";

import HeroHeaderSection from "@/components/blocks/landing/HeroHeaderSection";
import HeroImageSection from "@/components/blocks/landing/HeroImageSection";
import HeroFeaturesSection from "@/components/blocks/landing/HeroFeaturesSection";
import HeroTechnologiesSection from "@/components/blocks/landing/HeroTechnologiesSection";
import HeroFooterSection from "@/components/blocks/landing/HeroFooterSection";

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
