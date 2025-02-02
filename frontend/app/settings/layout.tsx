import { AppLayout } from "@/components/blocks/core/app-layout";

export default function PreferencesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AppLayout>{children}</AppLayout>;
}
