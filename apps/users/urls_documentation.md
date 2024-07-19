# API Documentation

This document provides details about the API endpoints for user management.

## Endpoints

### 1. `POST /registration/`
- **Description:** Register a new user.
- **Permissions:** AllowAny
- **Methods:**
  - `POST`: Create a new user. Requires request body with user registration data.
- **Request Body:**
  ```json
  {
    "username": "string",
    "name": "string",
    "surname": "string",
    "email": "string",
    "phone": "string",
    "is_lessor": "boolean",
    "password": "string",
    "re_password": "string"
  }
