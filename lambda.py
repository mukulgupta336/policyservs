import json
import smtplib
import os
from email.mime.text import MIMEText


def build_email_body(event):
    """Generate HTML email body based on type"""
    if event.get("type") == "contact":
        return f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #333; line-height:1.6; background:#f9f9f9; padding:20px;">
    <table style="max-width:600px; margin:auto; background:#fff; border-radius:8px; padding:20px; border:1px solid #ddd;">
      <tr>
        <td>
          <h2 style="color:#2c3e50; margin-bottom:10px;">📩 New Contact Request</h2>
          <p style="margin:0 0 15px 0;">You have received a new contact request from your website.</p>
          
          <table style="width:100%; border-collapse:collapse;">
            <tr>
              <td style="padding:8px; font-weight:bold; width:150px;">Name:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("name", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold;">Email:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("email", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold;">Phone:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("phone_number", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold;">Subject:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("subject", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold; vertical-align:top;">Message:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("message", "N/A")}</td>
            </tr>
          </table>

          <p style="margin-top:20px; font-size:12px; color:#888;">
            This email was automatically generated from your website contact form.
          </p>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

    elif event.get("type") == "get_quote":
        return f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #333; line-height:1.6; background:#f9f9f9; padding:20px;">
    <table style="max-width:600px; margin:auto; background:#fff; border-radius:8px; padding:20px; border:1px solid #ddd;">
      <tr>
        <td>
          <h2 style="color:#2c3e50; margin-bottom:10px;">📝 New Quote Request</h2>
          <p style="margin:0 0 15px 0;">A new insurance quote request has been submitted via your website.</p>
          
          <table style="width:100%; border-collapse:collapse;">
            <tr>
              <td style="padding:8px; font-weight:bold; width:150px;">Name:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("name", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold;">Email:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("email", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold;">Phone:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("phone_number", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold;">Insurance Type:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("insurance_type", "N/A")}</td>
            </tr>
            <tr>
              <td style="padding:8px; font-weight:bold; vertical-align:top;">Coverage Details:</td>
              <td style="padding:8px; background:#f5f5f5;">{event.get("coverage_details", "N/A")}</td>
            </tr>
          </table>

          <p style="margin-top:20px; font-size:12px; color:#888;">
            This email was automatically generated from your website quote form.
          </p>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

    # fallback
    return f"""
<html>
  <body style="font-family: Arial, sans-serif; padding:20px;">
    <p>{event.get("body", "Hello! This is a test email.")}</p>
  </body>
</html>
"""


def lambda_handler(event, context):
    sender = os.environ["GMAIL_USER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    recipient = "mukulgupta339@gmail.com"
    msg_type = event.get("type", "N/A")
    if msg_type == "contact":
        subject = "New Contact Request from " + event.get("name", "N/A")
    elif msg_type == "get_quote":
        subject = "New Quote Request from " + event.get("name", "N/A")
    else:
        subject = "Test Email"
    body = build_email_body(event)

    try:
        # Setup MIME
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()

        return {
            "statusCode": 200,
            "body": f"Email sent successfully"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

