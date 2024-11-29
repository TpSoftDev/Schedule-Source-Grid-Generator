import sys
import os
import requests

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

# Now use absolute imports
from controllers.api_calls.base_auth.base_auth import BaseAuth
from controllers.utils.URLs import URLs
from controllers.utils.credentials import load_creds


class ScheduleSourceAPI(BaseAuth):
    """Handles Schedule Source API interactions for employee global availability"""
    
    def __init__(self, auth_url: str, credentials: dict):
        # Initialize with test site authentication
        super().__init__(
            auth_url=auth_url,
            credentials=credentials
        )
        self.base_url = URLs.TEST_BASE_URL.value.rstrip('/')
        
        # Explicitly authenticate when creating the instance
        self.authenticate()

    def get_global_availability(self, employee_external_id):
        # Use the provided URL directly
        endpoint = "https://test.tmwork.net/2023.1/api/io/GlobalAvailDay/"
        
        # Define query parameters
        params = {
            "Fields": "AvailableRanges,DayId,FirstName,EmployeeExternalId",
            "EmployeeExternalId": employee_external_id
        }
        
        # Define headers
        headers = {
            "Cookie": "BuildCookie=24112919245101.7c...",
            "User-Agent": "PostmanRuntime/7.42.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "x-api-token": self.api_token,
            "x-session-id": self.session_id
        }
        
        # Make the GET request
        response = requests.get(endpoint, headers=headers, params=params)
        
        # Check the response
        if response.status_code == 200:
            print("✅ Request successful!")
            print(response.json())  # or response.text for raw data
        else:
            print("❌ Request failed!")
            print(f"Status Code: {response.status_code}")
            print(response.text)


# Main function to test the ScheduleSourceAPI
if __name__ == "__main__":
    # Load credentials
    creds = load_creds()
    credentials = {
        "code": creds.code,
        "user": creds.user,
        "password": creds.password
    }
    
    # Initialize ScheduleSourceAPI
    print("Testing ScheduleSourceAPI initialization and authentication...")
    api = ScheduleSourceAPI(URLs.TEST_SITE_AUTH.value, credentials)
    
    # Test authentication
    if api._is_authenticated:
        print("\n✅ Authentication successful!")
        print(f"Base URL: {api.base_url}")
        print(f"Session ID: {api.session_id}")
        print(f"API Token: {api.api_token}")
    else:
        print("\n❌ Authentication failed!")
    
    # Test the GET request
    employee_id = "223133927"
    api.get_global_availability(employee_id)