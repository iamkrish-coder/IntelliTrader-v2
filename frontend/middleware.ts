import { auth } from "./auth";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getToken } from "next-auth/jwt";

export async function middleware(request: NextRequest) {
  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET,
  });
  const isAuth = request.nextUrl.pathname.startsWith("/auth");

  // If they're on an auth page and are authenticated, redirect to dashboard
  if (isAuth && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // If they're not on an auth page and not authenticated, redirect to signin
  if (!isAuth && !token) {
    return NextResponse.redirect(new URL("/auth/signin", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/secure/:path*", "/auth/:path*", "/settings/:path*"],
};
