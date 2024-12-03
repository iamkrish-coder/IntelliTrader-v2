import AuthCredentialProvider from "@/components/build/AuthCredentialProvider";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <AuthCredentialProvider
          type="signin"
          title="Sign In"
          description="Welcome back! Please sign in to your account."
          action="Sign In"
        />
      </div>
    </div>
  );
}
