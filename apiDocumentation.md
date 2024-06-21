
## customUser views
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
   


## bloomfilter views


### Train Bloom Filter
**Purpose:** Trains the application's Bloom filter on a list of passwords provided in the POST request.

- **Method:** POST
- **Endpoint:** `/bloomfilter/train/`
- **Headers:** X-CSRFToken
- **Body:**
  ```json
  {
    "passwords": ["string1", "string2", ...],
    "size": 1000,
    "num_hashes": 15,
    "num_characters": int
  }
  ```
- **Success Response:**
  - **Code:** 201 Created
  - **Content:**
    ```json
    {
      "id": "integer",
      "size": "integer",
      "num_hashes": "integer",
      "num_characters": "integer",
      "bit_array": "string"
    }
    ```
- **Error Response:**
  - **Code:** 4XX/5XX (e.g., 400 BAD REQUEST, 500 INTERNAL SERVER ERROR)
  - **Content:** Error message detailing the issue.

### Test Password Against Bloom Filter
**Purpose:** Tests if a password is in the Bloom filter using a POST request.
pre-trained bloom filters ID are (12,13,14)
ID 12: corresponds to the bloom filter trained on the top 100 8 characters passwords from the rockyou.txt file
ID 13: corresponds to the bloom filter trained on the top 100 10 characters passwords from the rockyou.txt file
ID 14: corresponds to the bloom filter trained on the top 100 12 characters passwords from the rockyou.txt file
- **Method:** POST
- **Endpoint:** `/bloomfilter/test/<int:pk>/`
- **Headers:** X-CSRFToken
- **Body:**
  ```json
  {
    "password": "string",
    "threshold": 0.9
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "result": "boolean"
    }
    ```
- **Error Response:**
  - **Code:** 404 Not Found
  - **Content:** `{"error": "Bloom filter not found"}`
  - **Code:** 4XX/5XX (e.g., 400 BAD REQUEST, 500 INTERNAL SERVER ERROR)
  - **Content:** Error message detailing the issue.

### Get All Bloom Filters
**Purpose:** Returns all the Bloom filters that exist in the application with their information.

- **Method:** GET
- **Endpoint:** `/bloomfilter/all/`
- **Headers:** X-CSRFToken
- **Body:** None
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    [
      {
        "id": "integer",
        "size": "integer",
        "num_hashes": "integer",
        "num_characters": "integer",
        "bit_array": "string"
      },
      ...
    ]
    ```
- **Error Response:**
  - **Code:** 4XX/5XX (e.g., 404 NOT FOUND, 500 INTERNAL SERVER ERROR)
  - **Content:** Error message detailing the issue.

### Delete Bloom Filter
**Purpose:** Deletes a specific Bloom filter using its ID.

- **Method:** DELETE
- **Endpoint:** `/bloomfilter/delete/<int:pk>/`
- **Headers:** X-CSRFToken
- **Body:** None
- **Success Response:**
  - **Code:** 204 No Content
  - **Content:** None
- **Error Response:**
  - **Code:** 404 Not Found
  - **Content:** `{"error": "Bloom filter not found"}`
  - **Code:** 4XX/5XX (e.g., 400 BAD REQUEST, 500 INTERNAL SERVER ERROR)
  - **Content:** Error message detailing the issue.

### Calculate Jaccard Coefficient
**Purpose:** Returns the similarity percentage of two passwords using the Jaccard coefficient.

- **Method:** POST
- **Endpoint:** `/bloomfilter/jaccard/`
- **Headers:** X-CSRFToken
- **Body:**
  ```json
  {
    "password1": "string",
    "password2": "string"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "jaccard_similarity": "float"
    }
    ```
- **Error Response:**
  - **Code:** 400 Bad Request
  - **Content:** Error message detailing the issue.

