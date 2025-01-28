"use client";

import { AppSidebar } from "./AppSidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import Logo from "./AppLogo";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const getPageTitle = (path: string) => {
  const segment = path.split("/").pop() ?? "";
  const pathMappings: Record<string, string> = {
    dashboard: "",
    trading: "Trading",
    overview: "Overview",
    terminal: "Trading Terminal",
    profile: "Profile Settings",
    orders: "Order History",
    positions: "Positions",
    holdings: "Holdings",
  };

  return (
    pathMappings[segment] ?? segment.charAt(0).toUpperCase() + segment.slice(1)
  );
};

interface AppLayoutProps {
  children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const pathname = usePathname();
  const [currentPath, setCurrentPath] = useState(pathname);

  useEffect(() => {
    setCurrentPath(pathname);
  }, [pathname]);

  const rootSegment = pathname.split("/")[1] ?? ""; // Get the first segment (dashboard or trading)
  const rootTitle = rootSegment.charAt(0).toUpperCase() + rootSegment.slice(1);

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
          <div className="flex flex-1 items-center gap-4">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="h-6" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink href={`/${rootSegment}`}>
                    {rootTitle}
                  </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  <BreadcrumbPage>{getPageTitle(currentPath)}</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-4">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}
