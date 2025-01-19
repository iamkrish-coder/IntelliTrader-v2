import { NextRequest } from 'next/server';
import { sendEmail } from "@/lib/email";
import {
  VerificationEmailTemplate,
  VerificationEmailText,
} from "@/components/custom/VerificationEmailTemplate";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    
    // Add debugging
    console.log('Received email request:', {
      ...body,
      email: body.email ? 'REDACTED' : undefined
    });
    
    // Handle custom verification request format 
    if (body.email && body.url) {
      const callbackUrl = body.url;
      
      // Add debugging
      console.log('Sending verification email to:', body.email);
      
      const html = VerificationEmailTemplate({ callbackUrl });
      const text = VerificationEmailText({ callbackUrl });

      try {
        const result = await sendEmail({
          to: body.email,
          subject: "Sign In - IntelliTrader Account Verification",
          html,
          text,
        });
        
        console.log('Email sent successfully:', result.messageId);
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
