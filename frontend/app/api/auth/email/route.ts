import { NextRequest } from 'next/server';
import { sendEmail } from "@/lib/email";
import {
  VerificationEmailTemplate,
  VerificationEmailText,
} from "@/components/custom/email/VerificationEmailTemplate";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
      
    // Handle custom verification request format 
    if (body.email && body.url) {
      const callbackUrl = body.url;
      const html = VerificationEmailTemplate({ callbackUrl });
      const text = VerificationEmailText({ callbackUrl });

      try {
        const result = await sendEmail({
          to: body.email,
          subject: "Verify Your IntelliTrader Account",
          html,
          text,
        });
        
        return new Response(JSON.stringify({ success: true, messageId: result.messageId }));
      } catch (emailError) {
        console.error('Failed to send email:', emailError);
        throw emailError;
      }
    }

    // Handle direct email sending format
    const { to, subject, html, text } = body;

    if (!to || !subject || !html || !text) {
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
