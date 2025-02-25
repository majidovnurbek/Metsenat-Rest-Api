<img src="https://github.com/user-attachments/assets/0540d9f1-165a-4f44-9781-6a2739963917" alt="Image here" width="1280" height="400">

# Metsenat-Rest-Api

![Metsenat-API](https://img.shields.io/badge/Metsenat-API-blue.svg)

Metsenat-Rest-Api is a RESTful API designed for managing sponsorships and donations, facilitating transparent interactions between donors and recipients.

## 📌 Features
- User authentication and authorization
- Sponsor and student management
- Donation tracking and reporting
- Secure and optimized API endpoints

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- PostgreSQL (or any preferred database)
- Docker (optional but recommended)

### Installation (Windows, Linux, Mac)
1. Clone the repository:
   ```sh
   git clone git@github.com:majidovnurbek/Metsenat-Rest-Api.git
   cd Metsenat-Rest-Api
   ```

2. Create a virtual environment:
   - **Windows**
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Mac/Linux**
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update database and secret key values accordingly

### Database Migration
Run the following commands to set up the database:
```sh
python manage.py makemigrations
python manage.py migrate
```

### Running the Server
- **Windows, Mac, Linux:**
  ```sh
  python manage.py runserver
  ```

## 📂 Project Structure
```
Metsenat-Rest-Api/
├── .venv/                # Virtual environment
├── api/                  # Main API application
│   ├── migrations/       # Database migrations
│   │   ├── __init__.py
│   ├── admin.py         # Admin configuration
│   ├── apps.py          # App configuration
│   ├── managers.py      # Custom model managers
│   ├── models.py        # Database models
│   ├── serializers.py   # API serializers
│   ├── tests.py         # Unit tests
│   ├── urls.py          # API routes
│   ├── views.py         # API views
├── root/                 # Core project settings
│   ├── __init__.py
│   ├── asgi.py         # ASGI configuration
│   ├── settings.py     # Project settings
│   ├── urls.py         # Root URL configuration
│   ├── wsgi.py         # WSGI configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
```

## 🛠 API Endpoints
| Method | Endpoint                      | Description          |
|--------|-------------------------------|----------------------|
| GET    | `/sponsor/filter/`            | Filter sponsors     |
| DELETE | `/sponsor/update/{id}/`       | Delete sponsor      |
| PUT    | `/sponsor/update/{id}/`       | Update sponsor      |
| GET    | `/student/`                   | List students       |
| GET    | `/student/{id}/`               | Retrieve student    |
| POST   | `/student/add/`                | Add student        |
| GET    | `/student/filter/`            | Filter students     |
| DELETE | `/student/update/{id}/`       | Delete student      |
| GET    | `/student-sponsor/`           | List student sponsors |
| GET    | `/student-sponsor/{id}/`      | Retrieve student sponsor |

📖 Full API documentation is available via Swagger UI at:
```sh
http://localhost:8000/swagger/
```

## 🏗 Deployment

### Docker Setup (Optional)
1. Build and run the container:
   ```sh
   docker-compose up --build -d
   ```
2. Run database migrations:
   ```sh
   docker-compose exec web python manage.py migrate
   ```

### Gunicorn & Nginx (Production)
- Use Gunicorn for running the Django application.
- Set up Nginx as a reverse proxy for handling requests efficiently.

## 🛡 Security Best Practices
- Store sensitive credentials in environment variables.
- Use Django's built-in security middleware.
- Regularly update dependencies.

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Submit a pull request.

## 📜 License
This project is licensed under the MIT License.

## 📬 Contact
- **Author:** [majidovnurbek](https://github.com/majidovnurbek)
- **Email:** majidovnurbek613@gmail.com

---

Enjoy using **Metsenat-Rest-Api**! 🎉

