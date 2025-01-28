import { AppLayout } from "@/components/blocks/core/AppLayout";

export default function TradingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AppLayout>{children}</AppLayout>;
}
