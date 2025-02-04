"use client";

import { Preferences } from "@/lib/types/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { REGIONS } from "@/lib/config/constants";
import { Separator } from "@/components/ui/separator";

interface SystemSettingsProps {
  formData: Preferences;
  setFormData: (data: Preferences) => void;
}


export function SystemSettings({ formData, setFormData }: SystemSettingsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>System Preferences</CardTitle>
        <CardDescription>Configure system and region settings</CardDescription>
        <Separator />
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
                onValueChange={(value) =>
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
  );
}
