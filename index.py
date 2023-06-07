"""
This Script will Send All the Github Repo PR Data from last one week
"""

import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from jinja2 import Template
import requests

load_dotenv()
WEEK_AGO = datetime.datetime.now() - datetime.timedelta(days=7)

# https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# GitHub repository details
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_REPONAME = os.getenv('GITHUB_REPONAME')

# Email Notification Details
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
USER_EMAIL = os.getenv('USER_EMAIL')

# GitHub pull requests API Call for PRs
URL = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPONAME}/pulls'
PARAMS = {
    'state': 'all',
    'sort': 'created',
    'direction': 'desc'
}
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.raw+json',
    'Content-Type': 'application/json; charset=utf-8',
    'X-GitHub-Api-Version': '2022-11-28'
}

# Send API Call to GitHub for PRs
TIMEOUT = 5  # Set the desired timeout value (in seconds)
response = requests.get(URL, params=PARAMS, headers=HEADERS, timeout=TIMEOUT)
response.raise_for_status()
pull_requests = response.json()

filtered_pull_requests = [
    pr for pr in pull_requests
    if datetime.datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ') > WEEK_AGO
]

# Send only if there is data available in filtered_pull_requests
# Email body
if filtered_pull_requests:
    # Use HTML Template
    with open('template.html', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Provide dynamic data in template
    template = Template(template_content)
    email_body = template.render(
        GITHUB_USERNAME=GITHUB_USERNAME,
        GITHUB_REPONAME=GITHUB_REPONAME,
        PULL_REQUESTS=filtered_pull_requests
    )

    # Create the email content
    message = MIMEMultipart()
    message['Subject'] = f'PRs Summary for {GITHUB_USERNAME}/{GITHUB_REPONAME}'
    message['From'] = EMAIL_ADDRESS
    message['To'] = USER_EMAIL

    email_content = MIMEText(email_body, 'html')
    message.attach(email_content)

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)

    print('Email sent successfully.')
else:
    print('No pull requests available to send.')
