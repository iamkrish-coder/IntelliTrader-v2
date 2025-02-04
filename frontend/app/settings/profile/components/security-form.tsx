"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { useState } from "react"
import { toast } from "sonner"
import { Separator } from "@/components/ui/separator"

const securityFormSchema = z.object({
  currentPassword: z.string().min(8, "Password must be at least 8 characters."),
  newPassword: z.string().min(8, "Password must be at least 8 characters."),
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type SecurityFormValues = z.infer<typeof securityFormSchema>

const defaultValues: SecurityFormValues = {
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
}

export function SecurityForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false)

  const form = useForm<SecurityFormValues>({
    resolver: zodResolver(securityFormSchema),
    defaultValues,
    mode: "onChange",
  })

  async function onSubmit(data: SecurityFormValues) {
    setIsLoading(true)
    try {
      // TODO: Implement API call to update password
      console.log(data)
      toast.success("Password updated successfully")
      form.reset()
    } catch (error) {
      toast.error("Failed to update password")
    } finally {
      setIsLoading(false)
    }
  }

  const handleTwoFactorToggle = async (enabled: boolean) => {
    try {
      // TODO: Implement API call to toggle 2FA
      setTwoFactorEnabled(enabled)
      toast.success(`Two-factor authentication ${enabled ? 'enabled' : 'disabled'}`)
    } catch (error) {
      toast.error("Failed to update two-factor authentication")
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Security Information</CardTitle>
        <CardDescription>Manage your account security and authentication preferences</CardDescription>
        <Separator />
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Password Change Section */}
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Change Password</h4>
              <p className="text-sm text-muted-foreground">
                Update your password to maintain account security
              </p>
            </div>

            <Form {...form}>
              <div className="space-y-4">
                <FormField
                  control={form.control}
                  name="currentPassword"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Current Password</FormLabel>
                      <FormControl>
                        <Input
                          type="password"
                          className="max-w-md"
                          {...field}
                        />
                      </FormControl>
                    </div>
                  )}
                />

                <FormField
                  control={form.control}
                  name="newPassword"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">New Password</FormLabel>
                      <FormControl>
                        <Input
                          type="password"
                          className="max-w-md"
                          {...field}
                        />
                      </FormControl>
                    </div>
                  )}
                />

                <FormField
                  control={form.control}
                  name="confirmPassword"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Confirm Password</FormLabel>
                      <FormControl>
                        <Input
                          type="password"
                          className="max-w-md"
                          {...field}
                        />
                      </FormControl>
                    </div>
                  )}
                />

                <div className="flex justify-end">
                  <Button
                    type="button"
                    disabled={isLoading}
                    onClick={form.handleSubmit(onSubmit)}
                  >
                    {isLoading ? "Updating..." : "Update Password"}
                  </Button>
                </div>
              </div>
            </Form>
          </div>

          {/* Two-Factor Authentication Section */}
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Two-factor Authentication</h4>
              <p className="text-sm text-muted-foreground">
                Add an extra layer of security to your account
              </p>
            </div>

            <div className="grid grid-cols-[160px_1fr_auto] items-center gap-4">
              <div className="text-sm font-medium">Status</div>
              <div className="text-sm text-muted-foreground">
                {twoFactorEnabled
                  ? "Your account is protected by two-factor authentication"
                  : "Enable two-factor authentication for enhanced security"}
              </div>
              <Switch
                checked={twoFactorEnabled}
                onCheckedChange={handleTwoFactorToggle}
              />
            </div>
          </div>

          {/* Active Sessions Section */}
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Active Sessions</h4>
              <p className="text-sm text-muted-foreground">
                Manage your active sessions across devices
              </p>
            </div>

            <div className="grid grid-cols-[160px_1fr_auto] items-center gap-4">
              <div className="text-sm font-medium">Sessions</div>
              <div className="text-sm text-muted-foreground">
                View and manage your active sessions
              </div>
              <Button variant="outline">Manage Sessions</Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
