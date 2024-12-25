"""
credentials_manager.py

OVERVIEW:
    This module represents the credentials for user authentication needed to access the
    external API of schedule source. In order to get an api token and session id, the program must
    use these credentials to authenticate the user in schedule source.

FUNCTIONS AND CLASSES:
    - class Credentials:
        Represents a user's authentication credentials with fields for code, username, and password.

    - def load_creds():
        Creates and returns an instance of the `Credentials` class with hardcoded authentication
        information. Also logs the loaded credentials to the console for debugging purposes.

USAGE:
    This class is used by the base_auth.py
"""

class Credentials:
          def __init__(self, code, user, password):
                    self.code = code
                    self.user = user
                    self.password = password

def load_creds():
          creds = Credentials("isu", "btowle04", "6269")
          return creds