# API Documentation

This document provides details about the API endpoints for the rental announcement application.

## Endpoints

### 1. `GET /addresses/`
- **Description:** Retrieve a list of addresses.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `GET`: List all addresses.

### 2. `POST /addresses/`
- **Description:** Create a new address.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `POST`: Create a new address. Requires request body with address data.

### 3. `GET /address/<int:pk>/`
- **Description:** Retrieve a specific address by ID.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `GET`: Retrieve address with the given ID.

### 4. `PUT /address/<int:pk>/`
- **Description:** Update a specific address by ID.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `PUT`: Update address with the given ID. Requires request body with updated address data.

### 5. `DELETE /address/<int:pk>/`
- **Description:** Delete a specific address by ID.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `DELETE`: Delete address with the given ID.

### 6. `GET /announcement/`
- **Description:** Retrieve a list of announcements.
- **Permissions:** Authenticated users.
- **Methods:**
  - `GET`: List all announcements.

### 7. `POST /announcement/`
- **Description:** Create a new announcement.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `POST`: Create a new announcement. Requires request body with announcement data.

### 8. `GET /announcement/<int:pk>/`
- **Description:** Retrieve a specific announcement by ID.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `GET`: Retrieve announcement with the given ID.

### 9. `PUT /announcement/<int:pk>/`
- **Description:** Update a specific announcement by ID.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `PUT`: Update announcement with the given ID. Requires request body with updated announcement data.

### 10. `DELETE /announcement/<int:pk>/`
- **Description:** Delete a specific announcement by ID.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `DELETE`: Delete announcement with the given ID.

### 11. `GET /booking/`
- **Description:** Retrieve a list of bookings.
- **Permissions:** Authenticated users with Renter or Lessor role.
- **Methods:**
  - `GET`: List all bookings.

### 12. `POST /booking/`
- **Description:** Create a new booking.
- **Permissions:** Authenticated users with Renter or Lessor role.
- **Methods:**
  - `POST`: Create a new booking. Requires request body with booking data.

### 13. `GET /booking/<int:pk>/`
- **Description:** Retrieve a specific booking by ID.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `GET`: Retrieve booking with the given ID.

### 14. `PUT /booking/<int:pk>/`
- **Description:** Update a specific booking by ID.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `PUT`: Update booking with the given ID. Requires request body with updated booking data.

### 15. `DELETE /booking/<int:pk>/`
- **Description:** Delete a specific booking by ID.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `DELETE`: Delete booking with the given ID.

### 16. `PUT /booking/approve/<int:pk>/`
- **Description:** Approve a booking.
- **Permissions:** Authenticated users with Lessor role.
- **Methods:**
  - `PUT`: Approve booking with the given ID.

### 17. `PUT /booking/canceled/<int:pk>/`
- **Description:** Cancel a booking.
- **Permissions:** Authenticated users with Renter or Lessor role.
- **Methods:**
  - `PUT`: Cancel booking with the given ID.

### 18. `GET /booking/history/`
- **Description:** Retrieve a list of all bookings for the authenticated user.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `GET`: List all bookings for the authenticated user.

### 19. `POST /review/`
- **Description:** Create a new review.
- **Permissions:** Authenticated users.
- **Methods:**
  - `POST`: Create a new review. Requires request body with review data.

### 20. `GET /review/<int:pk>/`
- **Description:** Retrieve a specific review by ID.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `GET`: Retrieve review with the given ID.

### 21. `PUT /review/<int:pk>/`
- **Description:** Update a specific review by ID.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `PUT`: Update review with the given ID. Requires request body with updated review data.

### 22. `DELETE /review/<int:pk>/`
- **Description:** Delete a specific review by ID.
- **Permissions:** Authenticated users with Renter role.
- **Methods:**
  - `DELETE`: Delete review with the given ID.
