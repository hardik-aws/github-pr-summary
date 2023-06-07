# GitHub PRs Summary Email

This Python script obtains a list of the last week's open, closed, and in-draft PRs made in a GitHub repository. After using the GitHub API to retrieve the pull request data, it sends an email with the summary to a given email address.

## Prerequisites

- Python 3.x
- Requests library
- Jinja2 library
- python-dotenv library
- secure-smtplib library

## Setup

1. Clone or download this repository.

    ```bash
    git clone git@github.com:hardik-aws/github-pr-summery.git
    ```

2. Install the required Python libraries by running the following command:

    ```python
    pip3 install -r requirements.txt
    ```

3. Copy .`env.sample` file as a `.env` file

4. Set up the GitHub API access token:<br />
-- Generate a personal access token from your GitHub account settings.<br />
-- set token value in `.env` file as `GITHUB_TOKEN`<br />

5. Configure the email settings:<br />
-- Set the SMTP server and port of your email provider in the `.env` file as `SMTP_SERVER` and `SMTP_PORT`<br />
-- Update `EMAIL_ADDRESS` and `EMAIL_PASSWORD`  in the `.env` file for authentication.<br />
-- Specify the recipient's email address as the `USER_EMAIL` in the `.env` file.<br />

6. Set the target GitHub repository:<br />
-- Specify `GITHUB_USERNAME` and `GITHUB_REPONAME` with the owner's username and repository name in the `.env` file<br />

## Usage

- Run the Python script using the following command:

    ```python
    python index.py
    ```

This Python script obtains a list of the last week's open, closed, and in-draft PRs from the  GitHub repository. After using the GitHub API to retrieve the pull request data, it sends an email with the summary to a given email address.

## Customization

- Email Template: The email content is generated using an HTML template (`template.html`). You can customize the template according to your preference by modifying the HTML structure and styling.

- Email Subject: The subject of the email is defined in the script. Modify the `Subject` field in the `message` variable to change the subject line.
