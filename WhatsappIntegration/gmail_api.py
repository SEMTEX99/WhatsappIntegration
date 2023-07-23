import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery

class GmailAPI:
    """
    GmailAPI class, which handles Gmail API authentication and email processing, 
    returns the booking data 
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
    creds = None

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def is_booking_email(self, subject):
        return "New Booking for Your Accommodation" in subject

    def extract_booking_data(self, body):
        booking_data = {}
        lines = body.split("\n")
        for line in lines:
            if "Booking ID:" in line:
                booking_data["Booking ID"] = line.split(":")[1].strip()
            elif "Guest Name:" in line:
                booking_data["Guest Name"] = line.split(":")[1].strip()
            elif "Check-in Date:" in line:
                booking_data["Check-in Date"] = line.split(":")[1].strip()
            elif "Check-out Date:" in line:
                booking_data["Check-out Date"] = line.split(":")[1].strip()
            elif "Number of Guests:" in line:
                booking_data["Number of Guests"] = line.split(":")[1].strip()
            elif "Contact Email:" in line:
                booking_data["Contact Email"] = line.split(":")[1].strip()
            elif "Contact Phone:" in line:
                booking_data["Contact Phone"] = line.split(":")[1].strip()
        return booking_data