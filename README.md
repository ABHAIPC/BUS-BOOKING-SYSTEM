# Bus Reservation System

A streamlined web application for bus route management and ticket reservations. This platform provides distinct functionalities for both passengers and administrators, facilitating an efficient booking process and effective schedule management.

## Features

*   **User Authentication:** Secure sign-up, login, and logout functionalities for standard users and administrators.
*   **Ticket Booking:** Users can search for routes, view available schedules, and book bus tickets effortlessly.
*   **Admin Dashboard:** A dedicated interface for administrators to oversee operations securely.
*   **Route Management:** Admins can add and define new bus routes, specifying source, destination, distance, and estimated travel time.
*   **Schedule Management:** Admins can create and manage schedules for different buses and routes.
*   **Passenger Records:** Safely maintains passenger details and their respective reservations.

## Technology Stack

*   **Backend Framework:** Python, Flask
*   **Database & ORM:** SQLite, SQLAlchemy
*   **Security & Hashing:** Werkzeug Security Profiles
*   **Frontend templating:** HTML/CSS (Jinja2 Templates)

## Setup and Installation

### Prerequisites
*   Python 3.8+
*   pip (Python package installer)

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install Flask Flask-SQLAlchemy Werkzeug
    # Alternatively, if there is a requirements.txt file:
    # pip install -r requirements.txt
    ```

4.  **Configuration:**
    *   Initialize a new environment key: Replace the default `SECRET_KEY` in `app.py` or `.env` with a securely generated random secret key prior to production deployment.

5.  **Run the App Local Server:**
    ```bash
    python app.py
    ```
    Access the application via `http://127.0.0.1:5000/`.

## Architecture Overview

*   `app.py`: The entry point defining the routing architecture, state configurations, and view logic.
*   `models/`: Directory housing database schema definitions (e.g., Models for Bus, Route, Schedule, Passenger, User).
*   `templates/`: Directory containing semantic HTML templates providing the user interface layers.

## Usage Guide

*   **Users/Passengers:** Navigate to the main page to create an account. Once logged in, utilize the "Get Ticket" feature to browse routes, select schedules, and input passenger information for booking.
*   **Administrators:** Use the admin credentials to log into the system. Access the `/admin/dashboard` to begin administering the available bus routes and adding schedules to the public timetable.

## Security Considerations

*   **Secret Management:** Avoid committing hardcoded secret keys or production database URIs to source control. Use environment variables.
*   **Database:** This application utilizes SQLite primarily for development and demonstration context. For production, migrating to a robust RDBMS like PostgreSQL or MySQL is advised.

---
*Note: This repository provides an abstract structural pattern for a reservation system. Any specific environment keys, confidential data, or proprietary business details have been intentionally omitted to ensure safety on public version control networks.*
"# BUS-BOOKING-SYSTEM" 
