import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: [
      "lh3.googleusercontent.com", // Google OAuth profile pictures
      "avatars.githubusercontent.com", // GitHub profile pictures
    ],
  },
};

export default nextConfig;
