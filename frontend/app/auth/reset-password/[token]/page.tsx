import { Metadata } from "next";
import ResetPasswordForm from "../components/reset-password-form";

export const metadata: Metadata = {
  title: "Reset Password",
  description: "Enter your new password",
};

interface ResetPasswordPageProps {
  params: {
    token: string;
  };
}

export default function ResetPasswordPage({ params }: ResetPasswordPageProps) {
  return (
    <div className="container flex h-screen w-screen flex-col items-center justify-center">
      <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
        <ResetPasswordForm token={params.token} />
      </div>
    </div>
  );
}
