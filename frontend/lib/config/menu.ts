import {
  BarChart3,
  LineChart,
  Wallet,
  History,
  Settings,
  BookOpen,
  Bell,
  PieChart,
  Briefcase,
  TrendingUp,
} from "lucide-react";

export const Menu = {
  user: {
    name: "User",
    email: "user@intellitrader.com",
    avatar: "/avatars/default.jpg",
  },
  teams: [
    {
      account: "Zerodha",
      username: "ZWK399",
      logo: Wallet,
      plan: "Pro",
    },
  ],
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: BarChart3,
      isActive: true,
      items: [
        {
          title: "Overview",
          url: "/dashboard/overview",
        },
        {
          title: "Portfolio",
          url: "/dashboard/portfolio",
        },
        {
          title: "Positions",
          url: "/dashboard/positions",
        },
      ],
    },
    {
      title: "Trading",
      url: "/trading",
      icon: TrendingUp,
      isActive: true,
      items: [
        {
          title: "Terminal",
          url: "/trading/terminal",
        },
        {
          title: "Strategy Builder",
          url: "/trading/strategy",
        },
        {
          title: "Watchlist",
          url: "/trading/watchlist",
        },
        {
          title: "Orders",
          url: "/trading/orders",
        },
      ],
    },
    {
      title: "Analytics",
      url: "/analytics",
      icon: LineChart,
      items: [
        {
          title: "Performance",
          url: "/analytics/performance",
        },
        {
          title: "Reports",
          url: "/analytics/reports",
        },
      ],
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings,
      items: [
        {
          title: "Profile",
          url: "/settings/profile",
        },
        {
          title: "Preferences",
          url: "/settings/preferences",
        },
      ],
    },
  ],
  projects: [
    {
      name: "Documentation",
      url: "/docs",
      icon: BookOpen,
    },
  ],
};
