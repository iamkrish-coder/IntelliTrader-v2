"use client";

import HeroHeaderSection from "@/components/build/HeroHeaderSection";
import HeroImageSection from "@/components/build/HeroImageSection";
import HeroFeaturesSection from "@/components/build/HeroFeaturesSection";
import HeroTechnologiesSection from "@/components/build/HeroTechnologiesSection";
import HeroFooterSection from "@/components/build/HeroFooterSection";

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
