"use client";

import { useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Shell } from "lucide-react";
import { GeneralSettings } from "./components/general-settings";
import { TradeSettings } from "./components/trade-settings";
import { SystemSettings } from "./components/system-settings";
import { usePreferences } from "./hooks/use-preferences";

export default function PreferencesPage() {
  const {
    formData,
    setFormData,
    isLoading,
    status,
    handleSave,
    loadPreferences,
    loadedRef,
  } = usePreferences();

  // Load preferences when component mounts and session is available
  useEffect(() => {
    if (status === "authenticated" && !loadedRef.current) {
      loadedRef.current = true;
      loadPreferences();
    }
  }, [status, loadPreferences]);

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
          <GeneralSettings formData={formData} setFormData={setFormData} />
        </TabsContent>

        <TabsContent value="trade">
          <TradeSettings formData={formData} setFormData={setFormData} />
        </TabsContent>

        <TabsContent value="system">
          <SystemSettings formData={formData} setFormData={setFormData} />
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
