# Church Backend API Reference

## Base URL
`http://localhost:8000/api/v1`

## Authentication
All endpoints require authentication unless otherwise specified.

## Events

### Create Event
- **Endpoint**: `POST /events/`
- **Description**: Create a new event
- **Request Body**:
  ```json
  {
    "name": "Sunday Service",
    "description": "Weekly Sunday service with communion",
    "event_datetime": "2025-01-07T10:00:00",
    "location": "Main Sanctuary"
  }
  ```
- **Success Response (201 Created)**:
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Sunday Service",
    "description": "Weekly Sunday service with communion",
    "event_datetime": "2025-01-07T10:00:00",
    "location": "Main Sanctuary",
    "created_at": "2025-01-01T12:00:00"
  }
  ```

### List Events
- **Endpoint**: `GET /events/`
- **Query Parameters**:
  - `skip` (int, optional): Number of records to skip. Default: 0
  - `limit` (int, optional): Maximum number of records to return. Default: 20
- **Success Response (200 OK)**:
  ```json
  [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Sunday Service",
      "description": "Weekly Sunday service with communion",
      "event_datetime": "2025-01-07T10:00:00",
      "location": "Main Sanctuary",
      "created_at": "2025-01-01T12:00:00"
    }
  ]
  ```

### Get Event by ID
- **Endpoint**: `GET /events/{event_id}`
- **URL Parameters**:
  - `event_id` (UUID): ID of the event to retrieve
- **Success Response (200 OK)**:
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Sunday Service",
    "description": "Weekly Sunday service with communion",
    "event_datetime": "2025-01-07T10:00:00",
    "location": "Main Sanctuary",
    "created_at": "2025-01-01T12:00:00"
  }
  ```
- **Error Response (404 Not Found)**:
  ```json
  {
    "detail": "Event not found"
  }
  ```

## Images

### Upload Image
- **Endpoint**: `POST /images/`
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: Image file to upload
  - `description`: Description of the image
- **Success Response (201 Created)**:
  ```json
  {
    "id": "223e4567-e89b-12d3-a456-426614174001",
    "description": "Sunday Service January 2025",
    "image_url": "https://storage.example.com/images/sunday-service.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "width": 1920,
    "height": 1080,
    "created_at": "2025-01-01T12:00:00"
  }
  ```

### List Images
- **Endpoint**: `GET /images/`
- **Query Parameters**:
  - `skip` (int, optional): Number of records to skip. Default: 0
  - `limit` (int, optional): Maximum number of records to return. Default: 20
- **Success Response (200 OK)**:
  ```json
  [
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "description": "Sunday Service January 2025",
      "image_url": "https://storage.example.com/images/sunday-service.jpg",
      "file_size": 1024000,
      "mime_type": "image/jpeg",
      "width": 1920,
      "height": 1080,
      "created_at": "2025-01-01T12:00:00"
    }
  ]
  ```

### Get Grouped Images
- **Endpoint**: `GET /images/grouped`
- **Success Response (200 OK)**:
  ```json
    { 
    "year": {
        "2025": {
        "december": {
            "images": [
            {
                "description": "string",
                "id": "8cf9194c-de22-4fb0-a50d-71b7d4a8e789",
                "upload_date": "2025-12-31T11:15:13.498732Z",
                "image_url": "https://f005.backblazeb2.com/file/minitryChurch/da3c4e43-d5d0-499f-aad9-4f59090fec1a.png",
                "uploadthing_key": "da3c4e43-d5d0-499f-aad9-4f59090fec1a.png",
                "file_size": 60655,
                "mime_type": "image/png",
                "width": 268,
                "height": 151,
                "created_at": "2025-12-31T11:15:13.498732Z",
                "updated_at": null
            },
            {
                "description": "People standing",
                "id": "a298e282-4e57-45d5-95a7-19ce235b6db8",
                "upload_date": "2025-12-31T00:24:22.072663Z",
                "image_url": "https://f005.backblazeb2.com/file/minitryChurch/5962509f-28e7-433c-95b3-af81a46d97ba.png",
                "uploadthing_key": "5962509f-28e7-433c-95b3-af81a46d97ba.png",
                "file_size": 4126770,
                "mime_type": "image/png",
                "width": 2138,
                "height": 2305,
                "created_at": "2025-12-31T00:24:22.072663Z",
                "updated_at": null
            }
            ]
        }
        }
    }
    }
  ```

## Contact

### Send Contact Message
- **Endpoint**: `POST /contact/`
- **Description**: Send a contact form message
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, I have a question about your services."
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "message": "Your message has been sent successfully!"
  }
  ```

## Web

### Create Event with Images (Web Form)
- **Endpoint**: `POST /events`
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `name`: Event name (required)
  - `description`: Event description
  - `day`: Event date in YYYY-MM-DD format (required)
  - `time`: Event time in HH:MM format (required)
  - `location`: Event location (required)
  - `images`: One or more image files (optional)
- **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Event created successfully",
    "event_id": "123e4567-e89b-12d3-a456-426614174000",
    "image_urls": [
      "/static/uploads/event1.jpg"
    ]
  }
  ```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

#### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

#### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
