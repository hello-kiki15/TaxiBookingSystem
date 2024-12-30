# TaxiBookingSystem
A simple taxi booking system built using Python and SQLite.

## Features
- User registration and login system.
- Role-based dashboards for:
  - **Admin**: Manage users, view bookings.
  - **Driver**: View assigned bookings.
  - **Customer**: Book a taxi, view booking status.
- SQLite database for storing user and booking data.

## File Descriptions
- `admin_dashboard.py`: Handles the admin interface and operations.
- `driver_dashboard.py`: Manages the driver dashboard and booking assignments.
- `customer_dashboard.py`: Provides functionalities for customers to book taxis.
- `registrationpage.py`: Implements user registration features.
- `loginpage.py`: Contains login functionality.
- `TaxiBooking.db`: SQLite database file for storing user and booking data.

## How to Run
1. Clone this repository, navigate to the project directory, and run the main Python file to start the application:
   ```bash
   git clone https://github.com/your-username/TaxiBookingSystem.git
   cd TaxiBookingSystem
   python loginpage.py
