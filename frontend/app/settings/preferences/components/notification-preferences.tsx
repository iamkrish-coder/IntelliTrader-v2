"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { useState } from "react"
import { toast } from "sonner"

interface NotificationChannel {
  id: string
  label: string
  description: string
  enabled: boolean
}

interface NotificationType {
  id: string
  label: string
  description: string
  enabled: boolean
  channels: NotificationChannel[]
}

interface NotificationSettingsProps {
  formData: any
  setFormData: (data: any) => void
}

export function NotificationSettings({ formData, setFormData }: NotificationSettingsProps) {
  const [notifications, setNotifications] = useState<NotificationType[]>([
    {
      id: "trades",
      label: "Trade Alerts",
      description: "Get notified about order execution and trade updates",
      enabled: true,
      channels: [
        {
          id: "trades-email",
          label: "Email",
          description: "Receive trade notifications via email",
          enabled: true,
        },
        {
          id: "trades-push",
          label: "Push Notifications",
          description: "Receive trade notifications on your device",
          enabled: true,
        },
      ],
    },
    {
      id: "price",
      label: "Price Alerts",
      description: "Get notified when price targets are hit",
      enabled: true,
      channels: [
        {
          id: "price-email",
          label: "Email",
          description: "Receive price alerts via email",
          enabled: true,
        },
        {
          id: "price-push",
          label: "Push Notifications",
          description: "Receive price alerts on your device",
          enabled: true,
        },
      ],
    },
    {
      id: "portfolio",
      label: "Portfolio Updates",
      description: "Daily portfolio performance and summary",
      enabled: true,
      channels: [
        {
          id: "portfolio-email",
          label: "Email",
          description: "Receive portfolio updates via email",
          enabled: true,
        },
      ],
    },
  ])

  const handleToggleNotification = async (notificationId: string, enabled: boolean) => {
    try {
      // TODO: API call to update notification preference
      setNotifications(notifications.map(notification =>
        notification.id === notificationId
          ? { ...notification, enabled }
          : notification
      ))
      toast.success("Notification preferences updated")
    } catch (error) {
      toast.error("Failed to update notification preferences")
    }
  }

  const handleToggleChannel = async (
    notificationId: string,
    channelId: string,
    enabled: boolean
  ) => {
    try {
      // TODO: API call to update channel preference
      setNotifications(notifications.map(notification =>
        notification.id === notificationId
          ? {
              ...notification,
              channels: notification.channels.map(channel =>
                channel.id === channelId
                  ? { ...channel, enabled }
                  : channel
              ),
            }
          : notification
      ))
      toast.success("Channel preferences updated")
    } catch (error) {
      toast.error("Failed to update channel preferences")
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Notification Preferences</CardTitle>
        <CardDescription>Manage how you receive notifications and alerts</CardDescription>
        <Separator />
      </CardHeader>
      <CardContent>
        <div className="space-y-8">
          {notifications.map((notification) => (
            <div key={notification.id} className="space-y-4">
              <div className="grid grid-cols-[160px_1fr_100px] items-center gap-4 rounded-lg border p-4 bg-muted/50">
                <div>
                  <h4 className="text-base font-semibold">{notification.label}</h4>
                </div>
                <div className="space-y-0.5">
                  <div className="text-sm text-muted-foreground">
                    {notification.description}
                  </div>
                </div>
                <div className="flex justify-end">
                  <Switch
                    checked={notification.enabled}
                    onCheckedChange={(enabled) => handleToggleNotification(notification.id, enabled)}
                  />
                </div>
              </div>

              {notification.enabled && notification.channels.length > 0 && (
                <div className="ml-8 space-y-3">
                  {notification.channels.map((channel) => (
                    <div
                      key={channel.id}
                      className="grid grid-cols-[160px_1fr_100px] items-center gap-4"
                    >
                      <div className="text-sm font-medium">{channel.label}</div>
                      <div className="space-y-0.5">
                        <div className="text-sm text-muted-foreground">
                          {channel.description}
                        </div>
                      </div>
                      <div className="flex justify-start">
                        <Switch
                          className="data-[state=checked]:bg-muted-foreground data-[state=unchecked]:bg-muted"
                          checked={channel.enabled}
                          onCheckedChange={(enabled) =>
                            handleToggleChannel(notification.id, channel.id, enabled)
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
  )
} 