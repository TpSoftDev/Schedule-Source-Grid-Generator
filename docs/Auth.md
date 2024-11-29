# Authentication and Data Retrieval Process

## Authentication
- **BaseAuth Class**: 
  - Manages the authentication process by sending a POST request to the API's authentication endpoint.
  - Requires credentials: code, username, and password.
  - On successful authentication, it stores a `SessionId` and an `APIToken` for use in subsequent requests.

## Data Retrieval
- **ScheduleSourceAPI Class**: 
  - Extends `BaseAuth` to leverage the authentication tokens.
  - Uses the stored `SessionId` and `APIToken` to authenticate requests to the Schedule Source API.

- **get_global_availability Method**:
  - Fetches employee global availability data.
  - Ensures that the `SessionId` and `APIToken` are included in the request headers to authenticate the API call.