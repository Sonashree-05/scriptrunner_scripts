import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Retrieve environment variables
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
JIRA_USERNAME = os.environ['JIRA_USERNAME']
JIRA_URL = os.environ['JIRA_URL']
JIRA_PROJECT_KEY = os.environ['JIRA_PROJECT_KEY']

# Set up authentication and headers
auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# JQL query to find unassigned issues in the specified project
jql = f'project = {JIRA_PROJECT_KEY} AND assignee is EMPTY'
search_url = f'{JIRA_URL}/rest/api/3/search'

# Get unassigned issues
response = requests.get(
    search_url,
    headers=headers,
    auth=auth,
    params={'jql': jql}
)

if response.status_code != 200:
    print(f"Failed to search issues: {response.status_code} {response.text}")
    exit(1)

issues = response.json().get('issues', [])

for issue in issues:
    issue_key = issue['key']
    assign_url = f'{JIRA_URL}/rest/api/3/issue/{issue_key}/assignee'

    payload = json.dumps({
        'accountId': JIRA_USERNAME  # Using accountId for more robust identification
    })

    assign_response = requests.put(
        assign_url,
        headers=headers,
        auth=auth,
        data=payload
    )

    if assign_response.status_code == 204:
        print(f'Successfully assigned issue {issue_key} to {JIRA_USERNAME}')
    else:
        print(f'Failed to assign issue {issue_key}: {assign_response.status_code} {assign_response.text}')
