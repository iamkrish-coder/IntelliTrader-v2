"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import {
  LOG_LEVELS,
  QUEUE_TYPES,
  RUNTIME_INTERVALS,
  STRATEGIES,
  REGIONS,
  type LogLevel,
  type QueueType,
  type RuntimeInterval,
  type Strategy,
  type Region,
} from "@/lib/config/constants";
import api from "@/lib/http/fetch";
import { Shell } from "lucide-react";

interface PreferencesFormData {
  user_id?: string;
  debugger_mode: boolean;
  log_level: LogLevel;
  runtime_interval: RuntimeInterval;
  global_trade: boolean;
  historical_data_subscription: boolean;
  strategy: Strategy;
  live_trade: boolean;
  reset_app: boolean;
  prettier_print: boolean;
  topic_type: QueueType;
  queue_type: QueueType;
  secret_name: string;
  region_name: Region;
}

export default function PreferencesPage() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      // This will redirect to sign-in if not authenticated
      window.location.href = "/auth/signin";
    },
  });
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<PreferencesFormData>({
    debugger_mode: false,
    log_level: "DEBUG",
    runtime_interval: "5MINUTE",
    global_trade: true,
    historical_data_subscription: true,
    strategy: "001",
    live_trade: false,
    reset_app: false,
    prettier_print: false,
    topic_type: "FIFO",
    queue_type: "FIFO",
    secret_name: "IntelliTrader",
    region_name: "ap-south-1",
  });

  const handleSave = async () => {
    if (status === "loading") {
      return;
    }

    if (!session?.user?.id) {
      toast.error("Unable to save preferences. Please try signing in again.");
      return;
    }

    setIsLoading(true);
    try {
      console.log("Sending request with data:", {
        ...formData,
        user_id: session.user.id,
      });

      await api.post("/settings/preferences", {
        ...formData,
        user_id: session.user.id,
      });

      toast.success("Preferences saved successfully");
    } catch (error) {
      console.error("Failed to save preferences:", error);
      toast.error(
        error instanceof Error ? error.message : "Failed to save preferences",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Preferences</h1>
        <p className="text-muted-foreground">
          Configure your trading settings and preferences
        </p>
      </div>

      <Tabs defaultValue="general" className="space-y-4">
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="trade">Trade</TabsTrigger>
          <TabsTrigger value="system">System</TabsTrigger>
        </TabsList>

        <TabsContent value="general">
          <Card>
            <CardHeader>
              <CardTitle>General Settings</CardTitle>
              <CardDescription>
                Configure basic application settings
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex">
                <div className="flex-1 space-y-4 pr-8">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="debugger_mode" className="flex-1">
                      Debugger Mode
                    </Label>
                    <Switch
                      id="debugger_mode"
                      checked={formData.debugger_mode}
                      onCheckedChange={(checked) =>
                        setFormData({ ...formData, debugger_mode: checked })
                      }
                    />
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="reset_app" className="flex-1">
                      Reset App
                    </Label>
                    <Switch
                      id="reset_app"
                      checked={formData.reset_app}
                      onCheckedChange={(checked) =>
                        setFormData({ ...formData, reset_app: checked })
                      }
                    />
                  </div>
                </div>

                <div className="mx-8 h-full w-px bg-border" />

                <div className="flex-1 space-y-4 pl-8">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="prettier_print" className="flex-1">
                      Prettier Print
                    </Label>
                    <Switch
                      id="prettier_print"
                      checked={formData.prettier_print}
                      onCheckedChange={(checked) =>
                        setFormData({ ...formData, prettier_print: checked })
                      }
                    />
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="log_level" className="flex-1">
                      Log Level
                    </Label>
                    <Select
                      value={formData.log_level}
                      onValueChange={(value: LogLevel) =>
                        setFormData({ ...formData, log_level: value })
                      }
                    >
                      <SelectTrigger className="w-[180px]">
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
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="trade">
          <Card>
            <CardHeader>
              <CardTitle>Trade Settings</CardTitle>
              <CardDescription>
                Configure trading strategy preferences
              </CardDescription>
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
                      onValueChange={(value: QueueType) =>
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
                      onValueChange={(value: Strategy) =>
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
                        setFormData({ ...formData, global_trade: checked })
                      }
                    />
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="queue_type" className="flex-1">
                      Queue Type
                    </Label>
                    <Select
                      value={formData.queue_type}
                      onValueChange={(value: QueueType) =>
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
                      onValueChange={(value: RuntimeInterval) =>
                        setFormData({ ...formData, runtime_interval: value })
                      }
                    >
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select runtime interval" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.entries(RUNTIME_INTERVALS).map(
                          ([value, label]) => (
                            <SelectItem key={value} value={value}>
                              {label}
                            </SelectItem>
                          ),
                        )}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="system">
          <Card>
            <CardHeader>
              <CardTitle>System Settings</CardTitle>
              <CardDescription>
                Configure system and region settings
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex">
                <div className="flex-1 space-y-4 pr-8">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="secret_name" className="flex-1">
                      Secret Name
                    </Label>
                    <Input
                      id="secret_name"
                      value={formData.secret_name}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          secret_name: e.target.value,
                        })
                      }
                      className="w-[180px]"
                    />
                  </div>
                </div>

                <div className="mx-8 h-full w-px bg-border" />

                <div className="flex-1 space-y-4 pl-8">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="region_name" className="flex-1">
                      Region
                    </Label>
                    <Select
                      value={formData.region_name}
                      onValueChange={(value: Region) =>
                        setFormData({ ...formData, region_name: value })
                      }
                    >
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select region" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.entries(REGIONS).map(([value, label]) => (
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
        </TabsContent>
      </Tabs>

      <div className="mt-6 flex justify-end">
        <Button
          onClick={handleSave}
          disabled={isLoading || status === "loading"}
          className="min-w-[120px]"
        >
          {isLoading || status === "loading" ? (
            <>
              <Shell className="mr-2 h-4 w-4 animate-spin" />
              {status === "loading" ? "Loading..." : "Saving..."}
            </>
          ) : (
            "Save Changes"
          )}
        </Button>
      </div>
    </div>
  );
}
