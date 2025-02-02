"use client";

import HeroHeaderSection from "@/components/blocks/landing/hero-header-section";
import HeroImageSection from "@/components/blocks/landing/hero-image-section";
import HeroFeaturesSection from "@/components/blocks/landing/hero-features-section";
import HeroTechnologiesSection from "@/components/blocks/landing/hero-technologies-section";
import HeroFooterSection from "@/components/blocks/landing/hero-footer-section";

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
