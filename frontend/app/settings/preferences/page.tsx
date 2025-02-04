"use client";

import { useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Shell } from "lucide-react";

import { SystemSettings } from "./components/system-preferences";
import { usePreferences } from "./hooks/use-preferences";
import { NotificationSettings } from "./components/notification-preferences";
import { ApplicationPreferences } from "./components/application-preferences";

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
        <h3 className="text-3xl font-bold">Preferences</h3>
        <p className="text-muted-foreground">
          Configure your application and trading preferences
        </p>
      </div>

      <Tabs defaultValue="application" className="space-y-4">
        <TabsList>
          <TabsTrigger value="application">Application</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="system">System</TabsTrigger>
        </TabsList>

        <TabsContent value="application">
          <ApplicationPreferences formData={formData} setFormData={setFormData} />
        </TabsContent>

        <TabsContent value="notifications">
          <NotificationSettings formData={formData} setFormData={setFormData} />
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
