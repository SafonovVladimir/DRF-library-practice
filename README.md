# Library Management System API
This API is designed to manage books inventory, borrowing, customers, display notifications, and handle payments for a library. The system will optimize the work of library administrators and make the service more user-friendly.

# Installation
To install the Library Management System API, follow these steps:

1. Clone the repository:

```
git clone git@github.com:SafonovVladimir/DRF-library-practice.git

```
2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate

```
3. Install the requirements:

```
pip install -r requirements.txt
```
4. Run database migrations:
```
python manage.py migrate
```
5. Load initial data:
```
python manage.py loaddata library_db_data.json
```
6. Start the server:
```
python manage.py runserver
```
## Features
The Library Management System API provides the following features:

### Books Service
This service is responsible for managing the books inventory.

API:

- GET /books/: Get a list of all books.
- GET /books/<id>/: Get details about a specific book.
- POST /books/: Add a new book to the inventory.
- PUT /books/<id>/: Update an existing book's information.
- DELETE /books/<id>/: Delete a book from the inventory.
### Users Service
This service is responsible for managing the library customers.

API:

- POST /users/: Register a new user.
- POST /users/token/: Get a JWT token.
- POST /users/token/refresh/: Refresh a JWT token.
- GET /users/me/: Get the currently logged-in user's information.
- PUT /users/me/: Update the currently logged-in user's information.
### Borrowings Service
This service is responsible for managing the users' borrowings of books.

API:

- GET /borrowings/: Get a list of all borrowings.
- GET /borrowings/<id>/: Get details about a specific borrowing.
- POST /borrowings/: Add a new borrowing.
- PATCH /borrowings/<id>/: Update a borrowing's information.
- DELETE /borrowings/<id>/: Delete a borrowing.
### Payments Service
- This service is responsible for handling payments for book borrowings through the platform.

API:

- POST /payments/: Make a payment for a borrowing.
### Notifications Service (Telegram)
This service is responsible for sending notifications about new borrowing created, borrowings overdue, and successful payment. The notifications will be sent via Telegram.
