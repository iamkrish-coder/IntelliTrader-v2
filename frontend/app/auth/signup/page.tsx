import AuthCredentialProvider from "@/components/build/AuthCredentialProvider";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <AuthCredentialProvider
          type="signup"
          title="Sign Up"
          description="It's free to signup and only takes a minute."
          action="Create Account"
        />
      </div>
    </div>
  );
}
