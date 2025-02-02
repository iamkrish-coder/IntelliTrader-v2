"use client";

import { useState, useRef } from "react";
import { useSession } from "next-auth/react";
import { toast } from "sonner";
import { Preferences, ApiError } from "@/lib/types/api";
import api from "@/lib/http/fetch";

const defaultPreferences: Preferences = {
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
  is_active: true,
};

export function usePreferences() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      window.location.href = "/auth/signin";
    },
  });

  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<Preferences>(defaultPreferences);
  const loadedRef = useRef(false);

  const loadPreferences = async () => {
    if (!session?.user?.id) return;

    setIsLoading(true);
    try {
      const response = await api.get<Preferences>(
        `/settings/preferences/${session.user.id}`,
      );

      if (response) {
        setFormData(response);
        toast.success("Preferences loaded successfully");
      }
    } catch (error) {
      console.error("Error loading preferences:", error);
      if (error instanceof ApiError) {
        toast.error(error.getUserMessage());
      } else {
        toast.error("Failed to load preferences. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

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

  return {
    formData,
    setFormData,
    isLoading,
    status,
    handleSave,
    loadPreferences,
    loadedRef,
  };
}
