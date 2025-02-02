"use client";

import { Preferences } from "@/lib/types/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { LOG_LEVELS } from "@/lib/config/constants";

interface GeneralSettingsProps {
  formData: Preferences;
  setFormData: (data: Preferences) => void;
}

export function GeneralSettings({ formData, setFormData }: GeneralSettingsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>General Settings</CardTitle>
        <CardDescription>Configure basic application settings</CardDescription>
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
                  setFormData({
                    ...formData,
                    debugger_mode: checked,
                  })
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
                  setFormData({
                    ...formData,
                    prettier_print: checked,
                  })
                }
              />
            </div>

            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="log_level" className="flex-1">
                Log Level
              </Label>
              <Select
                value={formData.log_level}
                onValueChange={(value) =>
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
  );
}
