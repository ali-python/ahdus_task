AHDUS Task

## Overview
This project is a Django-based web application that manages projects and project members. It includes authentication, API endpoints, and unit tests to ensure proper functionality.

## Installation

### Prerequisites
- Python 3.8+
- Django 4+
- Django REST Framework
- PostgreSQL (or SQLite for local development)

### Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/project.git
   cd project
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a Superuser** (Optional, for admin access)
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

## Running Tests
To run the unit tests, use the following command:
```sh
python manage.py test
```

## API Endpoints
### Authentication
- **Login:** `POST /auth/login/`
- **Register:** `POST /auth/register/`
- **Logout:** `POST /logout/`

### Project Management
- **Create Project:** `POST /api/project/`
- **List Projects:** `GET /api/project/`
- **Add Member:** `POST /api/project/add_member/`

### Authentication in Tests
To authenticate a user in tests, use `APIClient`:
```python
from rest_framework.test import APIClient

def setUp(self):
    self.client = APIClient()
    self.user = CustomUser.objects.create_user(email="test@example.com", password="password")
    self.client.force_authenticate(user=self.user)
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

#######################################################################################################
##############################################Application Use###########################################
########################################################################################################

## Overview
This application provides a project management system where users can register, log in, and perform different actions based on their assigned roles. The owner can create projects, add members, and assign roles to control access to various endpoints.

## Features
- User Registration & Login
- Project Creation by Owners
- Role-Based Access Control
- Members assigned to projects with specific roles
- Role-specific API endpoints

## How to Use the Application
1. **Register a User**: Create an account by providing necessary details.
2. **Login**: Authenticate using credentials to receive an access token.
3. **Create a Project**: The project owner can create projects.
4. **Add Members**: The owner assigns users to the project with specific roles.
5. **Role-Based Access**: Users can access endpoints based on their assigned roles.

## API Endpoints
- **Authentication**
  - `POST auth/register/` - Register a new user
  - `POST auth/login/` - Login and receive an authentication token
  - `POST /logout/` - Logout and blacklist the token

- **Projects**
  - `POST api/projects/` - Create a project (Owner only)
  - `GET api/projects/` - List all projects (Role-based access)

- **Members**
  - `POST /projects/{project_id}/add-member/` - Add a member to a project (Owner only)
  - `GET /projects/{project_id}/members/` - List project members

- **Role-Based Access**
  - Users can access different endpoints based on their roles.

## Notes
Ensure that users authenticate before accessing protected endpoints. The owner manages project assignments, and members can interact with the system based on their roles.
