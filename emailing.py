import smtplib
import filetype
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# Load environment variables from .env file
load_dotenv()

# Email credentials and addresses
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SENDER = "tunderockson@gmail.com"
RECEIVER = "tunderockson@gmail.com"


# --- Sends an email with the captured image attached ---
def send_email(image_path):
    print("Started sending email")

    # Create the email object and set basic fields
    email_message = EmailMessage()
    email_message["Subject"] = "Motion Detected!"
    email_message.set_content(
        "Some movement has been noticed and caught on camera"
    )

    # Read the image file in binary mode
    with open(image_path, "rb") as file:
        content = file.read()

    # Detect the file type so the attachment gets the correct subtype
    kind = filetype.guess(image_path)

    # Attach the image to the email
    email_message.add_attachment(
        content,
        maintype="image",
        subtype=kind.extension
    )

    # --- Connect securely to Gmail SMTP server ---
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()          # Identify to the mail server
    gmail.starttls()      # Upgrade the connection to encrypted
    gmail.login(SENDER, PASSWORD)

    # Send the email
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

    print("Finished sending email")


# --- Allows the file to be run directly for testing ---
if __name__ == "__main__":
    send_email("images/19.png")