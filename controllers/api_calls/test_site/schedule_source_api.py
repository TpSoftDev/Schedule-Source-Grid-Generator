import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controllers.api_calls.base_auth.base_auth import BaseAuth
import requests
from controllers.utils.URLs import URLs
from controllers.utils.Paths import Paths
from controllers.utils.credentials import load_creds


class ScheduleSourceAPI(BaseAuth):
    """Handles Schedule Source API interactions for employee availability"""
    
    def __init__(self):
        # Load credentials
        creds = load_creds()
        
        # Initialize with test site authentication
        super().__init__(
            auth_url=URLs.TEST_SITE_AUTH.value,
            credentials={
                "code": creds.code,
                "user": creds.user,
                "password": creds.password
            }
        )
        self.base_url = URLs.TEST_BASE_URL.value

# Fetches an employee's availability ranges from Schedule Source
    def get_employee_availability(self, employee_id: str) -> dict:
              
        try:
            headers = self.get_auth_headers()
            
            # Define query parameters for the request
            params = {
                'Fields': 'AvailableRanges,EmployeeExternalId',
                'EmployeeExternalId': employee_id
            }
            
            response = requests.get(
                f"{self.base_url}{Paths.SS_AVAILABILITY.value}",
                headers=headers,
                params=params
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Schedule Source API Error: {str(e)}")
            raise

if __name__ == "__main__":
    # Test the API functionality
    schedule_source = ScheduleSourceAPI()
    test_employee_id = "223133927"
    
    availability = schedule_source.get_employee_availability(test_employee_id)
    print("Employee Availability:", availability)