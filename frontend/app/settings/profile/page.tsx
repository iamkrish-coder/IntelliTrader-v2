import { Separator } from "@/components/ui/separator";
import { ProfileForm } from "./components/profile-form";
import { SecurityForm } from "./components/security-form";

export default function SettingsProfilePage() {
  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h3 className="text-3xl font-bold">Profile Settings</h3>
        <p className="text-muted-foreground">
          Manage your account settings and trading preferences.
        </p>
      </div>

      <div className="space-y-6">
        {/* Personal Information Section */}
        <ProfileForm />

        {/* Security Settings Section */}
        <SecurityForm />
      </div>
    </div>
  );
}
