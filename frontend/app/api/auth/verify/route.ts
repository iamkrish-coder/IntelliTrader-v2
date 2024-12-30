import { signIn } from "@/auth";

export const runtime = "nodejs";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const token = searchParams.get('token');

  if (!token) {
    return Response.redirect('/auth/error?error=MissingToken');
  }

  try {
    // Mock verification for now - replace with your database logic
    const isTokenValid = true; // await db.tokens.verify(token);
    const userEmail = "user@example.com"; // await db.tokens.getEmail(token);
    
    if (isTokenValid) {
      // Sign in the user
      await signIn("credentials", {
        email: userEmail,
        redirect: true,
        callbackUrl: "/dashboard/profile"
      });
    }

    return Response.redirect('/auth/error?error=InvalidToken');
  } catch (error) {
    return Response.redirect('/auth/error?error=ServerError');
  }
} 