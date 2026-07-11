# boxly
Boxly is a storage management solution for consumers. Create a virtual inventory of real belongings, generate a QR code, place it on the box with your items and store it. Scan the QR code to see items in the box or utilize the app's search feature to easily locate items you put away.


## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- SQLite
- Pytest

## Features
- User registration and login
- JWT protected routes
- Locations, storage areas, boxes and items
- QR code generation for boxes
- Public QR lookup endpoint
- Backend tests

## Testing

Run tests from backend foloder:

```bash
cd backend
pytest -v
