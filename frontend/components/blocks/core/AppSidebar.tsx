"use client";

import * as React from "react";
import { useSidebar } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";

import { NavMain } from "@/components/blocks/core/NavMain";
import { NavProjects } from "@/components/blocks/core/NavProjects";
import { NavUser } from "@/components/blocks/core/NavUser";
import { TeamSwitcher } from "@/components/blocks/core/TeamSwitcher";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";
import { Menu } from "@/lib/config/menu";
import Logo from "./AppLogo";

interface AppSidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  menuConfig?: typeof Menu;
}

export function AppSidebar({ menuConfig = Menu, ...props }: AppSidebarProps) {
  const { state, toggleSidebar } = useSidebar();
  const isCollapsed = state === "collapsed";

  return (
    <Sidebar 
      collapsible="icon" 
      className="flex flex-col h-full overflow-hidden" 
      {...props}
    >
      <SidebarHeader className="shrink-0">
        <Logo collapsed={isCollapsed} className={isCollapsed ? "" : "my-2"} />
        <Separator orientation="horizontal" className="" />
        <TeamSwitcher teams={menuConfig.teams} />
        <Separator orientation="horizontal" className="" />
      </SidebarHeader>
      <SidebarContent className="flex-1 overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
        <NavMain items={menuConfig.navMain} />
        <NavProjects projects={menuConfig.projects} />
      </SidebarContent>
      <SidebarFooter className="shrink-0">
        <NavUser />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
