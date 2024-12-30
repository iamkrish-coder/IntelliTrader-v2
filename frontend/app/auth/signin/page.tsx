import SignInForm from "@/components/auth/SignInForm";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <SignInForm />
      </div>
    </div>
  );
}
