import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Logo from "@/components/build/Logo";

export default function VerifyRequestPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <Card>
          <CardHeader className="space-y-2">
            <Logo />
            <CardTitle className="text-2xl font-bold md:text-xl">
              Check your email
            </CardTitle>
            <CardDescription className="md:text-sm">
              A sign in link has been sent to your email address.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:gap-2">
            <p className="text-center text-sm text-muted-foreground">
              Please check your email for a sign in link. This link will expire
              in 24 hours.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
