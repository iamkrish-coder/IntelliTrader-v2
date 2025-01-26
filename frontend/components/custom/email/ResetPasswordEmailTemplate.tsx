interface ResetPasswordEmailProps {
  resetUrl: string;
}

export function ResetPasswordEmailTemplate({
  resetUrl,
}: ResetPasswordEmailProps) {
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Reset Your IntelliTrader Password</title>
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
              <svg height="1200px" width="1200px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                  viewBox="0 0 800 512" xml:space="preserve">
                  <polygon style="fill:#009E60;" points="145.976,45.272 291.944,466.728 0,466.728"/>
                  <polygon style="fill:#E21B1B;" points="366.024,466.728 220.056,45.272 512,45.272"/>
                  <polygon style="fill:#009E60;" points="585.976,45.272 731.944,466.728 440,466.728"/>
              </svg>
              <span>IntelliTrader .</span>
            </div>
          </div>
          <div class="content">
            <h2 style="color: #1e293b; margin-bottom: 16px;">Reset Your Password</h2>
            <p style="color: #475569; margin-bottom: 24px;">
              You recently requested to reset your password for your IntelliTrader account. Click the button below to reset it. This link will expire in 1 hour for security reasons.
            </p>
            <div style="text-align: center;">
              <a href="${resetUrl}" class="button">Reset Password</a>
            </div>
            <div class="divider"></div>
            <p style="color: #64748b; font-size: 14px;">
              If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.
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

export function ResetPasswordEmailText({ resetUrl }: ResetPasswordEmailProps) {
  return `
Reset Your IntelliTrader Password

You recently requested to reset your password for your IntelliTrader account. Click the following link to reset it:
${resetUrl}

This link will expire in 1 hour for security reasons.

If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.

${new Date().getFullYear()} IntelliTrader. All rights reserved.
  `;
} 