import { NextRequest, NextResponse } from "next/server";
import { authService } from "@/services/auth/authService";
import { PostgresLocalAdapter } from "@/lib/db/postgresLocalAdapter";

export async function GET(req: NextRequest) {
  try {

    const searchParams = new URL(req.url).searchParams;
    const token = searchParams.get('token');
    const email = searchParams.get('email');

    if (!token || !email) {
      return new Response('Missing token or email', { status: 400 });
    }

    const adapter = PostgresLocalAdapter();

    // Verify and consume token
    const verificationToken = await adapter.useVerificationToken({
      identifier: email,
      token
    });

    if (!verificationToken) {
      return NextResponse.json({ error: "Invalid or expired token" }, { status: 400 });
    }

    let user = await adapter.getUserByEmail(email);
    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 });
    }

    // Create a session for the user
    const session = await authService.createSession({
      userId: user.id,
      expires: new Date(Date.now() + 8 * 60 * 60 * 1000), // 8 hours
      sessionToken: token,
    });

    return NextResponse.json({ message: "User signed in successfully", session });
  } catch (error) {
    return NextResponse.json({ error: 'Error verifying email' }, { status: 500 });
  }
}