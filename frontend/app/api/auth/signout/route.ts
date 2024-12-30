import { signOut } from "@/auth";

export async function POST() {
  try {
    await signOut();
    return new Response(null, { status: 200 });
  } catch (error) {
    console.error("Error in signout route:", error);
    return new Response(null, { status: 500 });
  }
}
