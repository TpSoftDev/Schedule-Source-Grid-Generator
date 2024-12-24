# Schedule Source API
# This is the Schedule Source API class for handling employee availability data.
# It provides methods to interact with the Schedule Source API, specifically focusing on retrieving employee global availability information.
# It handles authentication, request management, and automatic token refresh.

#------------------------------------------------------------------------ Imports ------------------------------------------------------------------------#
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
from controllers.utils.Credentials import load_creds


#------------------------------------------------------------------------ Schedule Source API ------------------------------------------------------------------------#
class ScheduleSourceAPI(BaseAuth):
    """
    Schedule Source API client for handling employee availability data.
    
    This class provides methods to interact with the Schedule Source API,
    specifically focusing on retrieving employee global availability information.
    It handles authentication, request management, and automatic token refresh.
    
    Inherits from:
        BaseAuth: Provides base authentication functionality
    
    Attributes:
        base_url (str): Base URL for the Schedule Source API endpoints
        api_token (str): Current API token for authentication (inherited)
        session_id (str): Current session ID (inherited)
    """


    #------------------------------------------------------------------------ Constructor ------------------------------------------------------------------------#
    def __init__(self, auth_url: str, credentials: dict):
        """
        Initialize the Schedule Source API client.
        
        Args:
            auth_url (str): Authentication endpoint URL
            credentials (dict): Dictionary containing authentication credentials
                            Required keys: 'code', 'user', 'password'
        
        Note:
            Automatically authenticates upon initialization
        """
        super().__init__(auth_url=auth_url, credentials=credentials)
        self.base_url = URLs.TEST_BASE_URL.value.rstrip('/')
        self.authenticate()

    
    #------------------------------------------------------------------------ Get Global Availability ------------------------------------------------------------------------#
    def get_global_availability(self, EmployeeExternalId: str) -> dict:
        """
        Fetch an employee's global availability ranges from Schedule Source.
        
        Retrieves the availability schedule for a specific employee, including
        their available time ranges and basic information.
        
        Args:
            EmployeeExternalId (str): Unique identifier for the employee
        
        Returns:
            dict: JSON response containing employee availability data
                Format includes:
                - AvailableRanges: Time ranges when employee is available
                - EmployeeExternalId: Employee's unique identifier
                - DayId: Day identifier
                - FirstName: Employee's first name
        
        Raises:
            requests.exceptions.RequestException: If the API request fails
            

        """
        try:
            # Construct the endpoint URL
            endpoint = f"{self.base_url}{Paths.SS_AVAILABILITY.value}"
            print(f"\n[INFO] Endpoint URL: {endpoint}")

            # Set up headers with authentication tokens
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

            # Make the API request
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


#------------------------------------------------------------------------ Test section ------------------------------------------------------------------------#    
if __name__ == "__main__":
    """
    Test functionality of the ScheduleSourceAPI class.
    
    This section demonstrates the usage of the ScheduleSourceAPI by:
    1. Loading credentials from configuration
    2. Initializing the API client
    3. Testing authentication
    4. Retrieving employee availability data
    
    Example Usage:
        $ python schedule_source_api.py
    """
    # Load credentials and authenticate
    creds = load_creds()
    credentials = {
        "code": creds.code,
        "user": creds.user,
        "password": creds.password
    }

    # Initialize ScheduleSourceAPI
    api = ScheduleSourceAPI(URLs.TEST_SITE_AUTH.value, credentials)

    # Test authentication and availability retrieval
    if api.authenticate():
        print("\n✅ Authentication successful!")
        try:
            EmployeeExternalId = "170601496"
            print(f"\n[INFO] Fetching availability for EmployeeExternalId: {EmployeeExternalId}")
            availability = api.get_global_availability(EmployeeExternalId)
            print("\n[INFO] Employee Availability:", availability)
        except Exception as e:
            print("\n[ERROR] Failed to fetch employee availability:", e)
    else:
        print("\n❌ Authentication failed!")