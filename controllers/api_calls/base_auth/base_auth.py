import requests

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
        