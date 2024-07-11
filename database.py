import gspread
import streamlit as st
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

if "gcp_service_account" not in st.secrets:
    raise KeyError("Missing 'gcp_service_account' in secrets")

# Define the scope and credentials for Google Sheets API
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

# Extract credentials from secrets
creds_dict = st.secrets["gcp_service_account"]

# Ensure all required fields are available
required_keys = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
    "universe_domain"
]

for key in required_keys:
    if key not in creds_dict:
        raise KeyError(f"Missing '{key}' in 'gcp_service_account' secrets")

# Authenticate and create the service client
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


# Open the Google Sheet
sheet = client.open('BAU Database').sheet1

# Function to find the column index by name
def find_col(col_name):
    first_row = sheet.row_values(1)
    if col_name in first_row:
        col_index = first_row.index(col_name) + 1  # Convert from 0-indexed to 1-indexed
        return col_index
    return None

# Upsert function to update or insert email and new data
def upsert_email(email, new_data):
    #print(f"Email at beginning: {email}")
    try:
        email_col_index = find_col('Email')
        emails = sheet.col_values(email_col_index)[1:]
        #print(f"Emails: {emails}")

        if email in emails:
            row_index = emails.index(email) + 2  # +2 to account for 1-based index and header row
            current_row_values = sheet.row_values(row_index)

            # Ensure the new_data list is at least as long as the current row
            if len(new_data) < len(current_row_values):
                new_data.extend([''] * (len(current_row_values) - len(new_data)))
            elif len(new_data) > len(current_row_values):
                current_row_values.extend([''] * (len(new_data) - len(current_row_values)))

            updated_row_values = [
                new_data[i] if new_data[i] != '' else current_row_values[i]
                for i in range(len(current_row_values))
            ]
            sheet.update(f'A{row_index}', [updated_row_values])
            print(f"Email found. Row {row_index} updated successfully.")
        else:
            # Email does not exist, append a new row
            header_length = len(sheet.row_values(1))
            if len(new_data) < header_length:
                new_data.extend([''] * (header_length - len(new_data)))
            sheet.append_row(new_data)
            print("Email not found. New row added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# upsert_email('example@example.com', ['example@example.com', 'John', 'Doe', '123 Main St', 'Anytown', '12345'])
