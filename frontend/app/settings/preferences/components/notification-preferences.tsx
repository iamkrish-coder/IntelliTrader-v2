"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { Preferences } from "@/lib/types/api";

interface NotificationSettingsProps {
  formData: Preferences;
  setFormData: (data: Preferences) => void;
}

interface NotificationConfig {
  id: string;
  label: string;
  description: string;
  field: keyof Preferences;
  channels: {
    id: string;
    label: string;
    description: string;
    field: keyof Preferences;
  }[];
}

const NOTIFICATIONS_CONFIG: NotificationConfig[] = [
  {
    id: "trades",
    label: "Trade Alerts",
    description: "Get notified about order execution and trade updates",
    field: "notify_trades",
    channels: [
      {
        id: "trades-email",
        label: "Email",
        description: "Receive trade notifications via email",
        field: "notify_trades_email",
      },
      {
        id: "trades-push",
        label: "Push Notifications",
        description: "Receive trade notifications on your device",
        field: "notify_trades_push",
      },
    ],
  },
  {
    id: "price",
    label: "Price Alerts",
    description: "Get notified when price targets are hit",
    field: "notify_price_alerts",
    channels: [
      {
        id: "price-email",
        label: "Email",
        description: "Receive price alerts via email",
        field: "notify_price_alerts_email",
      },
      {
        id: "price-push",
        label: "Push Notifications",
        description: "Receive price alerts on your device",
        field: "notify_price_alerts_push",
      },
    ],
  },
  {
    id: "portfolio",
    label: "Portfolio Updates",
    description: "Daily portfolio performance and summary",
    field: "notify_portfolio",
    channels: [
      {
        id: "portfolio-email",
        label: "Email",
        description: "Receive portfolio updates via email",
        field: "notify_portfolio_email",
      },
    ],
  },
];

export function NotificationSettings({
  formData,
  setFormData,
}: NotificationSettingsProps) {
  const handleToggleNotification = (
    field: keyof Preferences,
    enabled: boolean,
  ) => {
    setFormData({
      ...formData,
      [field]: enabled,
      // If main notification is disabled, disable all its channels
      ...((!enabled &&
        NOTIFICATIONS_CONFIG.find((n) => n.field === field)?.channels.reduce(
          (acc, channel) => ({
            ...acc,
            [channel.field]: false,
          }),
          {},
        )) ||
        {}),
    });
  };

  const handleToggleChannel = (field: keyof Preferences, enabled: boolean) => {
    setFormData({ ...formData, [field]: enabled });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Notification Preferences</CardTitle>
        <CardDescription>
          Manage how you receive notifications and alerts
        </CardDescription>
        <Separator />
      </CardHeader>
      <CardContent>
        <div className="space-y-8">
          {NOTIFICATIONS_CONFIG.map((notification) => (
            <div key={notification.id} className="space-y-4">
              <div className="grid grid-cols-[160px_1fr_100px] items-center gap-4 rounded-lg border bg-muted/50 p-4">
                <div>
                  <h4 className="text-base font-semibold">
                    {notification.label}
                  </h4>
                </div>
                <div className="space-y-0.5">
                  <div className="text-sm text-muted-foreground">
                    {notification.description}
                  </div>
                </div>
                <div className="flex justify-end">
                  <Switch
                    checked={Boolean(formData[notification.field])}
                    onCheckedChange={(enabled) =>
                      handleToggleNotification(notification.field, enabled)
                    }
                  />
                </div>
              </div>

              {Boolean(formData[notification.field]) &&
                notification.channels.length > 0 && (
                  <div className="ml-8 space-y-3">
                    {notification.channels.map((channel) => (
                      <div
                        key={channel.id}
                        className="grid grid-cols-[160px_1fr_100px] items-center gap-4"
                      >
                        <div className="text-sm font-medium">
                          {channel.label}
                        </div>
                        <div className="space-y-0.5">
                          <div className="text-sm text-muted-foreground">
                            {channel.description}
                          </div>
                        </div>
                        <div className="flex justify-start">
                          <Switch
                            checked={Boolean(formData[channel.field])}
                            onCheckedChange={(enabled) =>
                              handleToggleChannel(channel.field, enabled)
                            }
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
