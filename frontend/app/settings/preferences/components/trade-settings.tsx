"use client";

import { Preferences } from "@/lib/types/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { QUEUE_TYPES, STRATEGIES, RUNTIME_INTERVALS } from "@/lib/config/constants";

interface TradeSettingsProps {
  formData: Preferences;
  setFormData: (data: Preferences) => void;
}

export function TradeSettings({ formData, setFormData }: TradeSettingsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Trade Settings</CardTitle>
        <CardDescription>Configure trading strategy preferences</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex">
          <div className="flex-1 space-y-4 pr-8">
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="live_trade" className="flex-1">
                Live Trading
              </Label>
              <Switch
                id="live_trade"
                checked={formData.live_trade}
                onCheckedChange={(checked) =>
                  setFormData({ ...formData, live_trade: checked })
                }
              />
            </div>

            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="topic_type" className="flex-1">
                Topic Type
              </Label>
              <Select
                value={formData.topic_type}
                onValueChange={(value) =>
                  setFormData({ ...formData, topic_type: value })
                }
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select topic type" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(QUEUE_TYPES).map(([value, label]) => (
                    <SelectItem key={value} value={value}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="strategy" className="flex-1">
                Strategy
              </Label>
              <Select
                value={formData.strategy}
                onValueChange={(value) =>
                  setFormData({ ...formData, strategy: value })
                }
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select strategy" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(STRATEGIES).map(([value, label]) => (
                    <SelectItem key={value} value={value}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="historical_data" className="flex-1">
                Historical Data
              </Label>
              <Switch
                id="historical_data"
                checked={formData.historical_data_subscription}
                onCheckedChange={(checked) =>
                  setFormData({
                    ...formData,
                    historical_data_subscription: checked,
                  })
                }
              />
            </div>
          </div>

          <div className="mx-8 h-full w-px bg-border" />

          <div className="flex-1 space-y-4 pl-8">
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="global_trade" className="flex-1">
                Global Trade
              </Label>
              <Switch
                id="global_trade"
                checked={formData.global_trade}
                onCheckedChange={(checked) =>
                  setFormData({
                    ...formData,
                    global_trade: checked,
                  })
                }
              />
            </div>

            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="queue_type" className="flex-1">
                Queue Type
              </Label>
              <Select
                value={formData.queue_type}
                onValueChange={(value) =>
                  setFormData({ ...formData, queue_type: value })
                }
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select queue type" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(QUEUE_TYPES).map(([value, label]) => (
                    <SelectItem key={value} value={value}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="runtime_interval" className="flex-1">
                Runtime Interval
              </Label>
              <Select
                value={formData.runtime_interval}
                onValueChange={(value) =>
                  setFormData({
                    ...formData,
                    runtime_interval: value,
                  })
                }
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select runtime interval" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(RUNTIME_INTERVALS).map(([value, label]) => (
                    <SelectItem key={value} value={value}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
