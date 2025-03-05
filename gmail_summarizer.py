import os
import json
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from transformers import pipeline

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    token_file = "token.json"
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)
 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_recent_emails(service, num_emails=2):  # Limit to 2 emails
    results = service.users().messages().list(userId='me', maxResults=num_emails, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    
    emails = {}
    
    for index, msg in enumerate(messages[:2]): 
        msg_id = msg['id']
        email_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        
        headers = email_data['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
        
        email_body = extract_email_body(email_data)
        
        emails[f"Email_{index+1}"] = {
            "subject": subject,
            "content": email_body
        }
    
    return emails

def extract_email_body(email_data):
    parts = email_data['payload'].get('parts', [])
    
    if not parts:
        return "No Content Available"

    for part in parts:
        if part['mimeType'] == 'text/plain':  
            body_data = part['body'].get('data', '')
            return base64.urlsafe_b64decode(body_data).decode("utf-8")

    return "No Content Available"

def summarize_text_t5(text):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="pt")
    summary_output = summarizer(text, min_length=5, max_length=500, do_sample=False)
    return summary_output[0]['summary_text']

def generate_summary_json(email_data):
    output_json = {}

    for email_id, data in email_data.items():
        extracted_text = data["content"]
        summary = summarize_text_t5(extracted_text)

        output_json[email_id] = {
            "subject": data["subject"],
            "content": extracted_text,
            "summary": summary
        }

    return output_json

def save_json_to_file(json_data, filename="Gmail_T5_Summary.json"):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Summarized emails saved in {filename}")

if __name__ == "__main__":
    gmail_service = authenticate_gmail()
    emails = get_recent_emails(gmail_service, num_emails=5)
    
    summarized_emails = generate_summary_json(emails)
    
    save_json_to_file(summarized_emails)
