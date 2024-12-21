class Credentials:
          def __init__(self, code, user, password):
                    self.code = code
                    self.user = user
                    self.password = password

def load_creds():
          creds = Credentials("isu", "btowle04", "6269")
          print(f"Loaded credentials: code={creds.code}, user={creds.user}, password={creds.password}")
          return creds