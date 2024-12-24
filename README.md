# Django Final Project Setup Instructions

## Clone the Repository

Clone the project repository using the following command:
```bash
git clone https://github.com/Laawrr/Django-FinalProj.git
```

## Set Up Virtual Environment

1. Create a virtual environment:
   ```bash
   python -m venv .\venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

## Install Requirements

1. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install additional packages:
   ```bash
   pip install Django
   pip install daphne
   pip install channels
   ```

## Configure Databases

Update the `DATABASES` settings in `settings.py` for both `finalProject` and `finalProject1` directories.

1. Open `settings.py` in both directories and locate the `DATABASES` configuration.
2. Replace it with the following:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'database_name',
           'USER': 'postgres',
           'PASSWORD': 'password',  
           'HOST': 'localhost',
           'PORT': '5432',  
       }
   }
   ```
   - Replace `database_name` with the name of your PostgreSQL database.
   - Replace `password` with your PostgreSQL password.

## Install Redis

Download and install Redis from the link below:
[Redis Releases on GitHub](https://github.com/tporadowski/redis/releases)

Follow the installation instructions for your operating system.

## Run the Program

### `finalProject`

Start the server for `finalProject`:

- Option 1: Using Django development server
  ```bash
  python manage.py runserver 8000
  ```

- Option 2: Using Daphne
  ```bash
  daphne -p 8000 finalProject.asgi:application
  ```

### `finalProject1`

Start the server for `finalProject1`:

- Option 1: Using Django development server
  ```bash
  python manage.py runserver 8001
  ```

- Option 2: Using Daphne
  ```bash
  daphne -p 8001 finalProject1.asgi:application
  ```

## Register and Log In

1. Open a web browser and navigate to:
   - `http://localhost:8000` for `finalProject`
   - `http://localhost:8001` for `finalProject1`

2. Register an account on the platform.
3. Log in using your credentials.

---

Follow these steps to set up and run the Django Final Project successfully.
