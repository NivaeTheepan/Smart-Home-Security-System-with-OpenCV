from twilio.rest import Client  # Twilio library for sending SMS
import os  # For environment variable access
from dotenv import load_dotenv  # For loading environment variables from a .env file
from datetime import datetime  # For working with dates and times

# Load environment variables from a .env file
load_dotenv()

# Twilio account credentials and phone numbers
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
SENDER = os.getenv("TWILIO_SEND_NUMBER")  # Twilio phone number
RECEIVER = os.getenv("TWILIO_RECEIVE_NUMBER")  # Recipient phone number

# Initialize Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_notification(url):
    """
    Sends an SMS notification with the motion detection details.
    """
    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")  # Format current timestamp
    client.messages.create(
        body=f"Person motion detected @{now}: {url}",
        from_=SENDER,
        to=RECEIVER
    )
