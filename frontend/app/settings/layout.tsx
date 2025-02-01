import { AppLayout } from "@/components/blocks/core/AppLayout";

export default function PreferencesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AppLayout>{children}</AppLayout>;
}
