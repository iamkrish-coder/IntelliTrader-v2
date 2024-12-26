import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "@/auth";

export async function middleware(request: NextRequest) {
  const session = await auth();

  // Skip middleware for auth callback routes
  if (request.nextUrl.pathname.startsWith("/api/auth/callback")) {
    return NextResponse.next();
  }

  // If the user is not logged in and trying to access a protected route
  if (!session && request.nextUrl.pathname.startsWith("/secure")) {
    const loginUrl = new URL("/auth/signin", request.url);
    loginUrl.searchParams.set("callbackUrl", request.url);
    return NextResponse.redirect(loginUrl);
  }

  // If the user is logged in and trying to access login or signup pages
  if (
    session &&
    (request.nextUrl.pathname === "/auth/signin" ||
      request.nextUrl.pathname === "/auth/signup")
  ) {
    return NextResponse.redirect(new URL("/dashboard/profile", request.url));
  }

  return NextResponse.next();
}

export const config = {
    matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
