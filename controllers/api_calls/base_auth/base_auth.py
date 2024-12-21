import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

import requests
from controllers.utils.Credentials import load_creds
from controllers.utils.URLs import URLs

class BaseAuth:
    """Base authentication class for all API interactions"""
    
    def __init__(self, auth_url, credentials):
        # Initialize with site-specific auth URL and credentials
        self.auth_url = auth_url
        self.credentials = credentials
        self.session_id = None
        self.api_token = None
        self._is_authenticated = False
        
    def authenticate(self):
        """Authenticates with the API and stores session tokens"""
        try:
            payload = {
                "ExternalId": "",
                "Request": {
                    "Portal": "mgr",
                    "Code": self.credentials["code"],
                    "Username": self.credentials["user"],
                    "Password": self.credentials["password"],
                }
            }

            headers = {
                "Content-Type": "application/json",
                "BuildCookie": "24060420361420.32735534d2ac453faeb6fc50bf314f4d",
            }

            response = requests.post(self.auth_url, headers=headers, json=payload)
            response.raise_for_status()
            
            response_json = response.json()
            self.session_id = response_json["Response"]["SessionId"]
            self.api_token = response_json["Response"]["APIToken"]
            self._is_authenticated = True
            
            return True

        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {str(e)}")
            self._is_authenticated = False
            return False

    def get_auth_headers(self):
        """Returns headers with authentication tokens"""
        if not self._is_authenticated:
            if not self.authenticate():
                raise Exception("Failed to authenticate with the API")
            
        return {
            "Content-Type": "application/json",
            "Authorization": self.api_token,
            "SessionId": self.session_id
        } 
        


#Test base_auth
if __name__ == "__main__":
    # Load credentials
    creds = load_creds()
    credentials = {
        "code": creds.code,
        "user": creds.user,
        "password": creds.password
    }
    
    # Initialize BaseAuth
    auth = BaseAuth(URLs.TEST_SITE_AUTH.value, credentials)
    
    # Test authentication
    print("Testing authentication...")
    success = auth.authenticate()
    
    if success:
        print("\n✅ Authentication successful!")
        print(f"Session ID: {auth.session_id}")
        print(f"API Token: {auth.api_token}")
        
        # Test getting headers
        headers = auth.get_auth_headers()
        print("\nAuthentication Headers:")
        for key, value in headers.items():
            print(f"{key}: {value}")
    else:
        print("\n❌ Authentication failed!")
        