import sys
import os
import requests

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

# Use absolute imports
from controllers.api_calls.base_auth.base_auth import BaseAuth
from controllers.utils.URLs import URLs
from controllers.utils.Paths import Paths
from controllers.utils.credentials import load_creds



class ScheduleSourceAPI(BaseAuth):
    """Handles Schedule Source API interactions for employee global availability."""
    
    def __init__(self, auth_url: str, credentials: dict):
        """Initialize with test site authentication and authenticate immediately."""
        super().__init__(auth_url=auth_url, credentials=credentials)
        self.base_url = URLs.TEST_BASE_URL.value.rstrip('/')
        self.authenticate()

    def get_global_availability(self, EmployeeExternalId: str) -> dict:
        """Fetch an employee's global availability ranges from Schedule Source."""
        try:
            # Construct the endpoint URL
            endpoint = f"{self.base_url}{Paths.SS_AVAILABILITY.value}"
            print(f"\n[INFO] Endpoint URL: {endpoint}")

            # Set up headers
            headers = {
                "Content-Type": "application/json",
                "x-api-token": self.api_token,
                "x-session-id": self.session_id,
                "BuildCookie": "24060420361420.32735534d2ac453faeb6fc50bf314f4d"
            }
            #print(f"[INFO] Headers: {headers}")

            # Define query parameters for the request
            params = {
                'Fields': 'AvailableRanges,EmployeeExternalId,DayId,FirstName',
                'EmployeeExternalId': EmployeeExternalId
            }

            # Make the request
            response = requests.get(endpoint, headers=headers, params=params)

            # Handle unauthorized access by re-authenticating
            if response.status_code == 401:
                print("\n[WARNING] Unauthorized. Re-authenticating...")
                self.authenticate()
                headers.update({
                    "x-api-token": self.api_token,
                    "x-session-id": self.session_id
                })
                print(f"[INFO] New Headers after re-authentication: {headers}")
                response = requests.get(endpoint, headers=headers, params=params)

                
                
            # Raise an error for bad responses
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # Log error details if a request exception occurs
            print(f"\n[ERROR] Schedule Source API Error: {str(e)}")
            if response:
                # Debugging information for the failed request
                print(f"[DEBUG] Request URL: {response.url}")
                print(f"[DEBUG] Response Status Code: {response.status_code}")
                print(f"[DEBUG] Response Headers: {response.headers}")
                if response.content:
                    print(f"[DEBUG] Response Content: {response.content.decode()}")
            raise  # Re-raise the exception to propagate the error


# Main function to test the ScheduleSourceAPI
if __name__ == "__main__":
    # Load credentials and authenticate
    creds = load_creds()
    credentials = {
        "code": creds.code,
        "user": creds.user,
        "password": creds.password
    }
    
    # Initialize ScheduleSourceAPI
    api = ScheduleSourceAPI(URLs.TEST_SITE_AUTH.value, credentials)
    
    # Authenticate and test get_global_availability
    if api.authenticate():
        print("\n✅ Authentication successful!")
        try:
            EmployeeExternalId = "944816917"  
            print(f"\n[INFO] Fetching availability for EmployeeExternalId: {EmployeeExternalId}")
            availability = api.get_global_availability(EmployeeExternalId)
            print("\n[INFO] Employee Availability:", availability)
        except Exception as e:
            print("\n[ERROR] Failed to fetch employee availability:", e)
    else:
        print("\n❌ Authentication failed!")