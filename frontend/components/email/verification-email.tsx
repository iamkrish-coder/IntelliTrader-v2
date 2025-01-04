interface VerificationEmailProps {
  callbackUrl: string;
}

export function VerificationEmailTemplate({
  callbackUrl,
}: VerificationEmailProps) {
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Sign in to IntelliTrader</title>
        <style>
          .container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: #ffffff;
          }
          .header {
            text-align: center;
            padding: 20px 0;
          }
          .logo {
            font-size: 24px;
            font-weight: bold;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .logo svg {
            width: 40px;
            height: 40px;
            margin-right: 8px;
          }
          .content {
            background: #f8fafc;
            border-radius: 8px;
            padding: 24px;
            margin: 20px 0;
          }
          .button {
            display: inline-block;
            padding: 12px 24px;
            background-color: #2563eb;
            color: white !important;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            margin: 20px 0;
          }
          .button:hover {
            background-color: #1d4ed8;
          }
          .footer {
            text-align: center;
            color: #64748b;
            font-size: 14px;
            margin-top: 20px;
          }
          .divider {
            border-top: 1px solid #e2e8f0;
            margin: 20px 0;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <div class="logo">
              <svg height="40" width="40" viewBox="0 0 800 512" xmlns="http://www.w3.org/2000/svg">
                <polygon style="fill:#009E60;" points="145.976,45.272 291.944,466.728 0,466.728"/>
                <polygon style="fill:#E21B1B;" points="366.024,466.728 220.056,45.272 512,45.272"/>
                <polygon style="fill:#009E60;" points="585.976,45.272 731.944,466.728 440,466.728"/>
              </svg>
              <span>IntelliTrader</span>
            </div>
          </div>
          <div class="content">
            <h2 style="color: #1e293b; margin-bottom: 16px;">Verify your email</h2>
            <p style="color: #475569; margin-bottom: 24px;">
              Click the button below to sign in to IntelliTrader. This link will expire in 24 hours.
            </p>
            <div style="text-align: center;">
              <a href="${callbackUrl}" class="button">Sign in to IntelliTrader</a>
            </div>
            <div class="divider"></div>
            <p style="color: #64748b; font-size: 14px;">
              If you didn't request this email, you can safely ignore it.
            </p>
          </div>
          <div class="footer">
            <p>IntelliTrader - Unleash the Power of Trading with Intelligence</p>
            <p style="color: #94a3b8;">${new Date().getFullYear()} IntelliTrader. All rights reserved.</p>
          </div>
        </div>
      </body>
    </html>
  `;
}

export function VerificationEmailText({ callbackUrl }: VerificationEmailProps) {
  return `
Sign in to IntelliTrader

Click the following link to sign in to your account:
${callbackUrl}

If you didn't request this email, you can safely ignore it.

${new Date().getFullYear()} IntelliTrader. All rights reserved.
  `;
}
