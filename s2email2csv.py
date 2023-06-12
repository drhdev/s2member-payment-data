import datetime
import pandas as pd
import imaplib
import email
import re
import csv
import os
import subprocess
from dotenv import load_dotenv
from dateutil.parser import parse

# Load environment variables from .env file
load_dotenv()

def extract_variables_from_email(email_body):
    variables = {
        'user_first_name': None,
        'user_last_name': None,
        'user_full_name': None,
        'user_email': None,
        'user_login': None,
        'user_ip': None,
        'user_id': None,
        'country': None,
        'subscr_id': None,
        'currency': None,
        'amount': None,
        'item_number': None,
        'item_name': None
    }

    lines = email_body.split('\n')
    for line in lines:
        if line.startswith('user_first_name:'):
            match = re.search(r'user_first_name:\s*(\w+)', line, re.IGNORECASE)
            if match:
                variables['user_first_name'] = match.group(1)
        elif line.startswith('user_last_name:'):
            match = re.search(r'user_last_name:\s*(\w+)', line, re.IGNORECASE)
            if match:
                variables['user_last_name'] = match.group(1)
        elif line.startswith('user_full_name:'):
            match = re.search(r'user_full_name:\s*(.*)', line, re.IGNORECASE)
            if match:
                variables['user_full_name'] = match.group(1)
        elif line.startswith('user_email:'):
            match = re.search(r'user_email:\s*(\S+)', line, re.IGNORECASE)
            if match:
                variables['user_email'] = match.group(1)
        elif line.startswith('user_login:'):
            match = re.search(r'user_login:\s*(\S+)', line, re.IGNORECASE)
            if match:
                variables['user_login'] = match.group(1)
        elif line.startswith('user_ip:'):
            match = re.search(r'user_ip:\s*(\S+)', line, re.IGNORECASE)
            if match:
                variables['user_ip'] = match.group(1)
        elif line.startswith('user_id:'):
            match = re.search(r'user_id:\s*(\d+)', line, re.IGNORECASE)
            if match:
                variables['user_id'] = match.group(1)
        elif line.startswith('country:'):
            match = re.search(r'country:\s*(.*)', line, re.IGNORECASE)
            if match:
                variables['country'] = match.group(1)
        elif line.startswith('subscr_id:'):
            match = re.search(r'subscr_id:\s*(\S+)', line, re.IGNORECASE)
            if match:
                variables['subscr_id'] = match.group(1)
        elif line.startswith('currency:'):
            match = re.search(r'currency:\s*(\S+)', line, re.IGNORECASE)
            if match:
                variables['currency'] = match.group(1)
        elif line.startswith('amount:'):
            match = re.search(r'amount:\s*([\d,\.]+)', line, re.IGNORECASE)
            if match:
                variables['amount'] = match.group(1)
        elif line.startswith('item_number:'):
            match = re.search(r'item_number:\s*(.*)', line, re.IGNORECASE)
            if match:
                variables['item_number'] = match.group(1)
        elif line.startswith('item_name:'):
            match = re.search(r'item_name:\s*(.*)', line, re.IGNORECASE)
            if match:
                variables['item_name'] = match.group(1)

    return variables

# IMAP settings
imap_host = os.getenv('IMAP_HOST')
imap_user = os.getenv('IMAP_USER')
imap_password = os.getenv('IMAP_PASSWORD')
inbox_folder = 'INBOX'

# Filter settings
subject_filter = '(s2Member / API Notification Email) - Payment'  # turn off with ''
sender_filter = ''  # turn on with 'sender@example.com'

# Output file
output_file = 'output.csv'

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_password)
imap.select(inbox_folder)

# Search for emails based on filters
search_criteria = []
if subject_filter:
    search_criteria.append(f'SUBJECT "{subject_filter}"')
if sender_filter:
    search_criteria.append(f'FROM "{sender_filter}"')
search_criteria_str = ' '.join(search_criteria)

status, data = imap.search(None, search_criteria_str)
email_ids = data[0].split()

# Process each email
processed_emails = []
for email_id in email_ids:
    status, data = imap.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    email_subject = msg['Subject']
    email_from = msg['From']
    email_date = parse(msg['Date']).strftime('%a, %d %b %Y')
    email_body = ''

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                email_body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        email_body = msg.get_payload(decode=True).decode('utf-8')

    extracted_variables = extract_variables_from_email(email_body)

    if extracted_variables:
        extracted_variables['email_subject'] = email_subject
        extracted_variables['email_from'] = email_from
        extracted_variables['email_date'] = email_date

        # Print extracted variables
        print('Extracted Variables:')
        for key, value in extracted_variables.items():
            print(f'{key}: {value}')
        print()

        processed_emails.append(extracted_variables)

# Append extracted variables to output.csv
if processed_emails:
    # Check if output.csv exists, and create it if it doesn't
    if not os.path.isfile(output_file):
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(processed_emails[0].keys()))
            writer.writeheader()

    with open(output_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(processed_emails[0].keys()))
        writer.writerows(processed_emails)

# Close IMAP connection
try:
    imap.close()
except imaplib.IMAP4.error:
    print("Failed to close the mailbox, it might already be closed.")
finally:
    imap.logout()
