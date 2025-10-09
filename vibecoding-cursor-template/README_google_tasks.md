# Google Tasks API Fetcher

This script fetches all active Google Tasks using the Google Tasks API with service account authentication.

## Setup

1. **Install Dependencies**
   ```bash
   pip3 install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
   ```

2. **Service Account Setup**
   - The service account credentials are stored in `Personal project/fluid-house-473920-i1-cfa125ad75e1.json`
   - This service account has been configured with Google Tasks API access

## Usage

Run the script to fetch all active Google Tasks:

```bash
python3 fetch_google_tasks.py
```

## What the Script Does

1. **Authentication**: Uses the service account credentials to authenticate with Google Tasks API
2. **Task List Discovery**: Fetches all available task lists
3. **Active Task Retrieval**: Gets all active (non-completed) tasks from each task list
4. **Display**: Shows formatted task information including:
   - Task title
   - Task list name
   - Notes (if any)
   - Due date (if set)
   - Last updated date
   - Task ID and status
5. **Export**: Saves all tasks to a timestamped JSON file for reference

## Output Example

```
✅ Successfully authenticated with Google Tasks API
🔄 Fetching all active Google Tasks...
📋 Found 1 task list(s)

📝 Processing task list: 'My Tasks'
   Found 0 active task(s)

📭 No active tasks found!
```

## Features

- **Service Account Authentication**: Secure authentication using service account credentials
- **Multiple Task Lists**: Supports fetching from all available task lists
- **Active Tasks Only**: Filters out completed tasks by default
- **Detailed Information**: Shows comprehensive task details
- **JSON Export**: Saves results to timestamped JSON files
- **Error Handling**: Graceful error handling for API issues

## API Permissions Required

The service account needs the following Google Tasks API scope:
- `https://www.googleapis.com/auth/tasks.readonly`

## Troubleshooting

1. **Authentication Issues**: Ensure the service account credentials file exists and is valid
2. **API Access**: Verify that the Google Tasks API is enabled for the project
3. **Permissions**: Check that the service account has the correct scopes
4. **Network**: Ensure internet connectivity for API calls

## File Structure

```
vibecoding-cursor-template/
├── fetch_google_tasks.py          # Main script
├── Personal project/
│   └── fluid-house-473920-i1-cfa125ad75e1.json  # Service account credentials
├── requirements.txt               # Updated with Google API dependencies
└── README_google_tasks.md        # This documentation
```

