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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useState } from "react"
import { toast } from "sonner"
import { Separator } from "@/components/ui/separator"

const profileFormSchema = z.object({
  fullName: z.string().min(2, "Name must be at least 2 characters."),
  email: z.string().email("Invalid email address."),
  phone: z.string().regex(/^\+?[1-9]\d{1,14}$/, "Invalid phone number."),
  timezone: z.string(),
  language: z.string(),
})

type ProfileFormValues = z.infer<typeof profileFormSchema>

const defaultValues: ProfileFormValues = {
  fullName: "",
  email: "",
  phone: "",
  timezone: "Asia/Kolkata",
  language: "en",
}

export function ProfileForm() {
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues,
    mode: "onChange",
  })

  async function onSubmit(data: ProfileFormValues) {
    setIsLoading(true)
    try {
      // TODO: Implement API call to update profile
      console.log(data)
      toast.success("Profile updated successfully")
    } catch (error) {
      toast.error("Failed to update profile")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Personal Information</CardTitle>
        <CardDescription>Manage your personal information and preferences</CardDescription>
        <Separator />
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Profile Picture</h4>
              <p className="text-sm text-muted-foreground">
                Your profile picture will be shown across the platform
              </p>
            </div>

            <div className="flex items-center gap-4">
              <Avatar className="h-24 w-24">
                <AvatarImage src="/avatars/default.jpg" alt="Profile" />
                <AvatarFallback>IN</AvatarFallback>
              </Avatar>
              <Button variant="outline">Change Avatar</Button>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Basic Information</h4>
              <p className="text-sm text-muted-foreground">
                Update your basic profile information
              </p>
            </div>

            <Form {...form}>
              <div className="space-y-4">
                <FormField
                  control={form.control}
                  name="fullName"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Full Name</FormLabel>
                      <FormControl>
                        <Input className="max-w-md" placeholder="John Doe" {...field} />
                      </FormControl>
                    </div>
                  )}
                />

                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Email</FormLabel>
                      <FormControl>
                        <Input className="max-w-md" placeholder="john@example.com" {...field} />
                      </FormControl>
                    </div>
                  )}
                />

                <FormField
                  control={form.control}
                  name="phone"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Phone Number</FormLabel>
                      <FormControl>
                        <Input className="max-w-md" placeholder="+91 9999999999" {...field} />
                      </FormControl>
                    </div>
                  )}
                />
              </div>
            </Form>
          </div>

          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium">Preferences</h4>
              <p className="text-sm text-muted-foreground">
                Configure your regional preferences
              </p>
            </div>

            <Form {...form}>
              <div className="space-y-4">
                <FormField
                  control={form.control}
                  name="timezone"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Timezone</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger className="max-w-md">
                            <SelectValue placeholder="Select timezone" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="Asia/Kolkata">India (GMT+5:30)</SelectItem>
                          <SelectItem value="UTC">UTC</SelectItem>
                          <SelectItem value="America/New_York">Eastern Time</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  )}
                />

                <FormField
                  control={form.control}
                  name="language"
                  render={({ field }) => (
                    <div className="grid grid-cols-[160px_1fr] items-center gap-4">
                      <FormLabel className="text-sm">Language</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger className="max-w-md">
                            <SelectValue placeholder="Select language" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="en">English</SelectItem>
                          <SelectItem value="hi">Hindi</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  )}
                />
              </div>
            </Form>
          </div>

          <div className="flex justify-end">
            <Button 
              type="button" 
              disabled={isLoading}
              onClick={form.handleSubmit(onSubmit)}
            >
              {isLoading ? "Saving..." : "Save Changes"}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 