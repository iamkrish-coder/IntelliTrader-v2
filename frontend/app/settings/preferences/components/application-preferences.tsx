"use client";

import { Preferences } from "@/lib/types/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  LOG_LEVELS, 
  QUEUE_TYPES, 
  STRATEGIES, 
  RUNTIME_INTERVALS 
} from "@/lib/config/constants";
import { Separator } from "@/components/ui/separator";

interface ApplicationPreferencesProps {
  formData: Preferences;
  setFormData: (data: Preferences) => void;
}

export function ApplicationPreferences({ formData, setFormData }: ApplicationPreferencesProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Application Preferences</CardTitle>
        <CardDescription>Configure your application and trading preferences</CardDescription>
        <Separator />
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* General Settings Section */}
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">General Configuration</h4>
              <p className="text-sm text-muted-foreground">
                Configure basic application settings
              </p>
            </div>

            <div className="grid grid-cols-2 gap-8">
              <div className="space-y-4">
                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="debugger_mode" className="text-sm">Debugger Mode</Label>
                  <Switch
                    id="debugger_mode"
                    checked={formData.debugger_mode}
                    onCheckedChange={(checked) =>
                      setFormData({
                        ...formData,
                        debugger_mode: checked,
                      })
                    }
                  />
                </div>

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="reset_app" className="text-sm">Reset App</Label>
                  <Switch
                    id="reset_app"
                    checked={formData.reset_app}
                    onCheckedChange={(checked) =>
                      setFormData({ ...formData, reset_app: checked })
                    }
                  />
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="prettier_print" className="text-sm">Prettier Print</Label>
                  <Switch
                    id="prettier_print"
                    checked={formData.prettier_print}
                    onCheckedChange={(checked) =>
                      setFormData({
                        ...formData,
                        prettier_print: checked,
                      })
                    }
                  />
                </div>

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="log_level" className="text-sm">Log Level</Label>
                  <Select
                    value={formData.log_level}
                    onValueChange={(value) =>
                      setFormData({ ...formData, log_level: value })
                    }
                  >
                    <SelectTrigger className="max-w-md">
                      <SelectValue placeholder="Select log level" />
                    </SelectTrigger>
                    <SelectContent>
                      {Object.entries(LOG_LEVELS).map(([value, label]) => (
                        <SelectItem key={value} value={value}>
                          {label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          </div>

          <Separator />

          {/* Trading Settings Section */}
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Trading Configuration</h4>
              <p className="text-sm text-muted-foreground">
                Configure trading strategy preferences
              </p>
            </div>

            <div className="grid grid-cols-2 gap-8">
              <div className="space-y-4">
                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="live_trade" className="text-sm">Live Trading</Label>
                  <Switch
                    id="live_trade"
                    checked={formData.live_trade}
                    onCheckedChange={(checked) =>
                      setFormData({ ...formData, live_trade: checked })
                    }
                  />
                </div>

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="topic_type" className="text-sm">Topic Type</Label>
                  <Select
                    value={formData.topic_type}
                    onValueChange={(value) =>
                      setFormData({ ...formData, topic_type: value })
                    }
                  >
                    <SelectTrigger className="max-w-md">
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

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="strategy" className="text-sm">Strategy</Label>
                  <Select
                    value={formData.strategy}
                    onValueChange={(value) =>
                      setFormData({ ...formData, strategy: value })
                    }
                  >
                    <SelectTrigger className="max-w-md">
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

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="historical_data" className="text-sm">Historical Data</Label>
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

              <div className="space-y-4">
                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="global_trade" className="text-sm">Global Trade</Label>
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

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="queue_type" className="text-sm">Queue Type</Label>
                  <Select
                    value={formData.queue_type}
                    onValueChange={(value) =>
                      setFormData({ ...formData, queue_type: value })
                    }
                  >
                    <SelectTrigger className="max-w-md">
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

                <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                  <Label htmlFor="runtime_interval" className="text-sm">Runtime Interval</Label>
                  <Select
                    value={formData.runtime_interval}
                    onValueChange={(value) =>
                      setFormData({
                        ...formData,
                        runtime_interval: value,
                      })
                    }
                  >
                    <SelectTrigger className="max-w-md">
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
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 