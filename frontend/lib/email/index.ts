import { createTransport } from "nodemailer";

console.log("Email configuration:", {
  host: process.env.EMAIL_SERVER_HOST,
  port: process.env.EMAIL_SERVER_PORT,
  user: process.env.EMAIL_SERVER_USER,
  from: process.env.EMAIL_FROM,
  // Don't log password for security
});

const transporter = createTransport({
  host: process.env.EMAIL_SERVER_HOST,
  port: Number(process.env.EMAIL_SERVER_PORT),
  secure: process.env.EMAIL_SERVER_PORT === "465",
  auth: {
    user: process.env.EMAIL_SERVER_USER,
    pass: process.env.EMAIL_SERVER_PASSWORD,
  },
  tls: {
    // Required for Gmail
    ciphers: "SSLv3",
    rejectUnauthorized: false,
  },
});

// Verify transporter configuration
transporter.verify((error, success) => {
  if (error) {
    console.error("SMTP connection error:", error);
  } else {
    console.log("SMTP server is ready");
  }
});

export const sendEmail = async ({
  to,
  subject,
  html,
  text,
}: {
  to: string;
  subject: string;
  html: string;
  text: string;
}) => {
  try {
    console.log("Attempting to send email:", {
      from: process.env.EMAIL_FROM,
      to,
      subject,
      hasHtml: !!html,
      hasText: !!text,
    });

    const info = await transporter.sendMail({
      from: process.env.EMAIL_FROM,
      to,
      subject,
      text,
      html,
    });

    console.log("Email sent successfully:", {
      messageId: info.messageId,
      response: info.response,
    });

    return info;
  } catch (error) {
    console.error("Failed to send email. Error details:", {
      name: error instanceof Error ? error.name : "Unknown",
      message: error instanceof Error ? error.message : "Unknown error",
      stack: error instanceof Error ? error.stack : undefined,
    });
    throw new Error(
      error instanceof Error ? error.message : "Failed to send email",
    );
  }
};
