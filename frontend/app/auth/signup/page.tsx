import SignUpForm from "@/components/auth/SignUpForm";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200 p-4">
      <div className="w-full max-w-[400px] md:max-w-[350px]">
        <SignUpForm />
      </div>
    </div>
  );
}
