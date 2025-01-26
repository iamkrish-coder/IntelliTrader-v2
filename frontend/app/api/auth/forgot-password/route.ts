import { NextResponse } from "next/server";
import { randomBytes } from "crypto";
import { PrismaClient } from "@prisma/client";
import { sendEmail } from "@/lib/email";
import { ResetPasswordEmailTemplate, ResetPasswordEmailText } from "@/components/custom/email/ResetPasswordEmailTemplate";

const prisma = new PrismaClient();

export async function POST(req: Request) {
  try {
    const { email } = await req.json();

    // Check if user exists
    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      // Return success even if user doesn't exist for security
      return NextResponse.json({
        success: true,
        message: "If an account exists with that email, a password reset link will be sent.",
      });
    }

    // Generate a secure random token
    const token = randomBytes(32).toString("hex");

    // Store the token with 1-hour expiration
    const expires = new Date(Date.now() + 3600000); // 1 hour from now
    await prisma.verificationToken.create({
      data: {
        identifier: email,
        token,
        expires,
      },
    });

    // Generate reset URL
    const resetUrl = `${process.env.NEXTAUTH_URL}/auth/reset-password/${token}`;

    // Send the reset email
    await sendEmail({
      to: email,
      subject: "Reset Your IntelliTrader Password",
      html: ResetPasswordEmailTemplate({ resetUrl }),
      text: ResetPasswordEmailText({ resetUrl }),
    });

    return NextResponse.json({
      success: true,
      message: "Password reset email sent successfully",
    });
  } catch (error) {
    console.error("Password reset error:", error);
    return NextResponse.json(
      { error: "Failed to process password reset request" },
      { status: 500 },
    );
  } finally {
    await prisma.$disconnect();
  }
} 