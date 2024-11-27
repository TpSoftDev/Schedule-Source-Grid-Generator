class Credentials:
          def __init__(self, code, user, password):
                    self.code = code
                    self.user = user
                    self.password = password

def load_creds():
          creds = Credentials("isu", "btowle04", "6269")
          return creds