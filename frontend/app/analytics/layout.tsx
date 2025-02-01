import { AppLayout } from "@/components/blocks/core/AppLayout";

export default function AnalyticsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AppLayout>{children}</AppLayout>;
}
