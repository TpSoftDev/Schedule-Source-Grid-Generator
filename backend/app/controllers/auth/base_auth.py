#------------------------------------------------------------------------ Imports ------------------------------------------------------------------------#
import os
import sys
from pathlib import Path

#------------------------------------------------------------------------ Path Setup ------------------------------------------------------------------------#
# Get the absolute path of the current file and resolve any symlinks
# Then navigate up 2 levels to reach the project root:
# base_auth.py -> auth -> controllers -> app -> [project_root]
root_dir = Path(__file__).resolve().parents[2]

# Add the project root to Python's path
# This allows Python to find our modules regardless of where the script is run from
sys.path.append(str(root_dir))

# Now we can import our local modules
import requests
from utils.Credentials import load_creds
from utils.URLs import URLs

#------------------------------------------------------------------------ BaseAuth Class ------------------------------------------------------------------------#
class BaseAuth:
    """Base authentication class for all API interactions"""
    
    def __init__(self, auth_url, credentials):
        # Initialize with site-specific auth URL and credentials
        self.auth_url = auth_url
        self.credentials = credentials
        self.session_id = None
        self.api_token = None
        self._is_authenticated = False

#------------------------------------------------------------------------ Authenticate ------------------------------------------------------------------------#
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
        
#------------------------------------------------------------------------ Get Auth Headers ------------------------------------------------------------------------#
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
        


#------------------------------------------------------------------------ Test base_auth ------------------------------------------------------------------------#
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
        