#!/usr/bin/env python3
"""
Google Tasks API Fetcher
Fetches all active Google Tasks using service account authentication.
"""

import json
import os
from datetime import datetime
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv


class GoogleTasksFetcher:
    def __init__(self, credentials_file=None):
        """Initialize the Google Tasks API client."""
        self.credentials_file = credentials_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate using OAuth2 credentials from environment."""
        try:
            # Load environment variables
            load_dotenv()
            
            # Define the scope for Google Tasks API
            scopes = ['https://www.googleapis.com/auth/tasks.readonly']
            
            # Try OAuth2 first (from GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
            
            if client_id and client_secret:
                print("🔑 Using OAuth2 credentials from environment variables")
                credentials = self._oauth2_flow(client_id, client_secret, scopes)
                if credentials:
                    self.service = build('tasks', 'v1', credentials=credentials)
                    print("✅ Successfully authenticated with Google Tasks API using OAuth2")
                    return
                
            # Try JSON format OAuth2 credentials (from GMAIL env variable)
            gmail_credentials = os.getenv('GMAIL')
            if gmail_credentials:
                try:
                    print("🔑 Using OAuth2 credentials from GMAIL environment variable")
                    # Parse the JSON credentials from environment
                    creds_data = json.loads(gmail_credentials)
                    credentials = Credentials.from_authorized_user_info(creds_data, scopes)
                    
                    # Build the service
                    self.service = build('tasks', 'v1', credentials=credentials)
                    print("✅ Successfully authenticated with Google Tasks API using OAuth2")
                    return
                except json.JSONDecodeError:
                    print("⚠️  GMAIL environment variable is not valid JSON format")
                except Exception as e:
                    print(f"⚠️  Error with OAuth2 credentials: {e}")
            
            # Fallback to service account if OAuth2 not available
            if self.credentials_file and os.path.exists(self.credentials_file):
                print("🔑 Using service account credentials")
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_file, scopes=scopes
                )
                self.service = build('tasks', 'v1', credentials=credentials)
                print("✅ Successfully authenticated with Google Tasks API using service account")
                return
            
            raise Exception("No valid credentials found. Please set GMAIL environment variable or provide service account file.")
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            raise
    
    def _oauth2_flow(self, client_id, client_secret, scopes):
        """Handle OAuth2 flow for user authentication."""
        try:
            # Create OAuth2 client config
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            # Check if we have existing tokens
            token_file = 'google_tasks_token.json'
            credentials = None
            
            if os.path.exists(token_file):
                print("🔄 Loading existing OAuth2 tokens...")
                credentials = Credentials.from_authorized_user_file(token_file, scopes)
            
            # If there are no (valid) credentials available, let the user log in
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    print("🔄 Refreshing expired OAuth2 tokens...")
                    credentials.refresh(Request())
                else:
                    print("🌐 Starting OAuth2 flow - browser will open for authorization...")
                    flow = InstalledAppFlow.from_client_config(client_config, scopes)
                    credentials = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                print("💾 Saving OAuth2 tokens for future use...")
                with open(token_file, 'w') as token:
                    token.write(credentials.to_json())
            
            return credentials
            
        except Exception as e:
            print(f"❌ OAuth2 flow failed: {e}")
            return None
    
    def get_task_lists(self):
        """Get all task lists."""
        try:
            tasklists = self.service.tasklists().list().execute()
            print(f"🔍 Debug: Raw tasklists response: {tasklists}")
            return tasklists.get('items', [])
        except HttpError as e:
            print(f"❌ Error fetching task lists: {e}")
            print(f"🔍 Debug: Full error details: {e.content if hasattr(e, 'content') else 'No content'}")
            return []
    
    def get_tasks_from_list(self, tasklist_id, show_completed=True):
        """Get all tasks from a specific task list."""
        try:
            # Fetch tasks - can show completed or just active tasks
            tasks = self.service.tasks().list(
                tasklist=tasklist_id,
                showCompleted=show_completed,
                showHidden=False
            ).execute()
            return tasks.get('items', [])
        except HttpError as e:
            print(f"❌ Error fetching tasks from list {tasklist_id}: {e}")
            return []
    
    def fetch_all_active_tasks(self):
        """Fetch all active tasks from all task lists."""
        print("🔄 Fetching all active Google Tasks...")
        
        # Get all task lists
        task_lists = self.get_task_lists()
        if not task_lists:
            print("📝 No task lists found")
            return []
        
        print(f"📋 Found {len(task_lists)} task list(s)")
        
        all_tasks = []
        
        for tasklist in task_lists:
            tasklist_id = tasklist['id']
            tasklist_title = tasklist.get('title', 'Untitled')
            
            print(f"\n📝 Processing task list: '{tasklist_title}'")
            
            # Get active tasks from this list
            active_tasks = self.get_tasks_from_list(tasklist_id, show_completed=False)
            
            # Get all tasks (including completed) for debugging
            all_tasks_in_list = self.get_tasks_from_list(tasklist_id, show_completed=True)
            
            print(f"   Found {len(active_tasks)} active task(s)")
            print(f"   Found {len(all_tasks_in_list)} total task(s) (including completed)")
            
            # Add task list info to each task
            for task in active_tasks:
                task['tasklist_title'] = tasklist_title
                task['tasklist_id'] = tasklist_id
            
            all_tasks.extend(active_tasks)
        
        return all_tasks
    
    def format_task_info(self, task):
        """Format task information for display."""
        title = task.get('title', 'Untitled')
        notes = task.get('notes', '')
        due_date = task.get('due', '')
        updated = task.get('updated', '')
        tasklist_title = task.get('tasklist_title', 'Unknown List')
        
        # Format dates if present
        if due_date:
            try:
                due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        if updated:
            try:
                updated = datetime.fromisoformat(updated.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        return {
            'title': title,
            'notes': notes,
            'due_date': due_date,
            'updated': updated,
            'tasklist': tasklist_title,
            'id': task.get('id', ''),
            'position': task.get('position', ''),
            'status': task.get('status', 'needsAction')
        }
    
    def display_tasks(self, tasks):
        """Display tasks in a formatted way."""
        if not tasks:
            print("\n📭 No active tasks found!")
            return
        
        print(f"\n📋 Total Active Tasks: {len(tasks)}")
        print("=" * 80)
        
        for i, task in enumerate(tasks, 1):
            task_info = self.format_task_info(task)
            
            print(f"\n{i}. {task_info['title']}")
            print(f"   📁 List: {task_info['tasklist']}")
            
            if task_info['notes']:
                print(f"   📝 Notes: {task_info['notes']}")
            
            if task_info['due_date']:
                print(f"   📅 Due: {task_info['due_date']}")
            
            if task_info['updated']:
                print(f"   🔄 Updated: {task_info['updated']}")
            
            print(f"   🆔 ID: {task_info['id']}")
            print(f"   📊 Status: {task_info['status']}")


def main():
    """Main function to fetch and display Google Tasks."""
    # Path to the service account credentials file (fallback)
    credentials_file = 'Personal project/fluid-house-473920-i1-cfa125ad75e1.json'
    
    try:
        # Initialize the fetcher (will try OAuth2 first, then service account)
        fetcher = GoogleTasksFetcher(credentials_file)
        
        # Fetch all active tasks
        tasks = fetcher.fetch_all_active_tasks()
        
        # Display the tasks
        fetcher.display_tasks(tasks)
        
        # Save to JSON file for reference
        if tasks:
            output_file = f'active_tasks_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Tasks saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return


if __name__ == "__main__":
    main()
