import { NextRequest } from "next/server";
import { sendEmail } from "@/lib/email";
import {
  VerificationEmailTemplate,
  VerificationEmailText,
} from "@/components/email/verification-email";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  console.log("Email API route hit");

  try {
    const body = await req.json();
    console.log("Request body:", body);

    // Handle NextAuth verification request format
    if (body.email) {
      console.log("Processing verification email request for:", body.email);

      const callbackUrl = `http://localhost:3000/auth/verify?token=${Math.random().toString(36).substring(2)}`;
      const html = VerificationEmailTemplate({ callbackUrl });
      const text = VerificationEmailText({ callbackUrl });

      const result = await sendEmail({
        to: body.email,
        subject: "Sign in to IntelliTrader",
        html,
        text,
      });

      console.log("Verification email sent successfully:", result);
      return new Response(
        JSON.stringify({
          success: true,
          messageId: result.messageId,
          response: result.response,
        }),
        {
          status: 200,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    // Handle direct email sending format
    const { to, subject, html, text } = body;

    if (!to || !subject || !html || !text) {
      console.error("Missing required fields:", {
        to,
        subject,
        hasHtml: !!html,
        hasText: !!text,
      });
      return new Response(
        JSON.stringify({
          error: "Missing required fields",
          details: {
            to: !to ? "missing" : "ok",
            subject: !subject ? "missing" : "ok",
            html: !html ? "missing" : "ok",
            text: !text ? "missing" : "ok",
          },
        }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    const result = await sendEmail({ to, subject, html, text });
    console.log("Email sent successfully:", result);

    return new Response(
      JSON.stringify({
        success: true,
        messageId: result.messageId,
        response: result.response,
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      },
    );
  } catch (error) {
    console.error("Email API error:", {
      name: error instanceof Error ? error.name : "Unknown",
      message: error instanceof Error ? error.message : "Unknown error",
      stack: error instanceof Error ? error.stack : undefined,
    });

    return new Response(
      JSON.stringify({
        error: "Failed to send email",
        details: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    );
  }
}
