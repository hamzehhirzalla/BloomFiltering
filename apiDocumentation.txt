
### Register a New User
**Purpose:** Registers a new user to the application after checking if the password is weak or leaked using a Bloom filter.

- **Method:** POST
- **Endpoint:** `/accounts/register/`
- **Headers:** X-CSRFToken
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 201 Created
  - **Content:** User registration details
  ```json
  {
    "username": "string"
}
  ```
- **Error Responses:**
  - **Code:** 400 Bad Request
    - **Content:** `{"error": "Password is too weak, choose a stronger one"}`
  - **Code:** 404 Not Found
    - **Content:** `{"error": "Bloom filter not found"}`

### Login an Existing User
**Purpose:** Logs in an existing user to the application.

- **Method:** POST
- **Endpoint:** `/accounts/login/`
- **Headers:** X-CSRFToken
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** `{"message": "User logged in successfully"}`
- **Error Response:**
  - **Code:** 401 Unauthorized
    - **Content:** `{"message": "Invalid credentials"}`

### Get Current User Information
**Purpose:** Retrieves information of the currently authenticated user.

- **Method:** GET
- **Endpoint:** `/accounts/current_user/`
- **Headers:** Authorization: Token `<token>`, X-CSRFToken
- **Body:** None
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** User details
  ```json
  {
    "username": "string",
    ...
  }
  ```
- **Error Response:**
  - **Code:** 403 Forbidden
    - **Content:** `{"detail": "Authentication credentials were not provided."}`

### Logout a User
**Purpose:** Logs out a currently authenticated user from the application.

- **Method:** POST
- **Endpoint:** `/accounts/logout/`
- **Headers:** Authorization: Token `<token>`,X-CSRFToken
- **Body:** None
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** `{"message": "Logged out successfully"}`

### Change Password
**Purpose:** Changes the password of an authenticated user after checking if the new password is weak or slightly modified.

- **Method:** POST
- **Endpoint:** `/accounts/change-password/`
- **Headers:** Authorization: Token `<token>`,X-CSRFToken
- **Body:**
  ```json
  {
    "old_password": "string",
    "new_password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** `{"success": "Password changed successfully"}`
- **Error Responses:**
  - **Code:** 400 Bad Request
    - **Content:** `{"error": "Invalid old password"}`
  - **Code:** 400 Bad Request
    - **Content:** `{"error": "Password is too weak, choose a stronger one"}`
  - **Code:** 404 Not Found
    - **Content:** `{"error": "Bloom filter not found"}`
