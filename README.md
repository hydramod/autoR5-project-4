# autoR5 Car Rental System

Welcome to **autoR5**, a comprehensive car rental system developed for a fictional car rental company based in Dublin. This system allows users to browse, book, and manage vehicle rentals of various classes, providing a seamless and user-friendly experience for both customers and administrators.

## Project Overview

**autoR5** is designed to facilitate the rental process, from vehicle selection to payment and booking management. It empowers our fictional car rental company to efficiently manage its vehicle fleet and customer reservations.

## Key Features

- **Vehicle Catalog**: Browse and search for vehicles by class, location, and availability.
- **User Registration and Authentication**: Users can create accounts, sign in, and manage their profiles.
- **Booking**: Users can book vehicles, specifying rental dates and locations.
- **Availability Checking**: Real-time availability checking to prevent overbooking.
- **Pricing**: Dynamic pricing based on vehicle class and rental duration.
- **Conflict Resolution**: Avoids booking conflicts by checking for overlapping rental dates.
- **Payment Integration**: Secure payment processing with the Stripe payment gateway.
- **Booking Management**: Customers can view and manage their bookings.
- **Admin Panel**: Administrative tools for managing vehicles, bookings, and user data.

## Project Structure

This repository contains the Django project and application files that make up the **autoR5** car rental system. The project is organized as follows:

- **autoR5/**: The main project directory containing settings, URLs, and project-level configurations.
- **autoR5/app/**: The Django app directory containing the core functionality, including models, views, and templates.
- **autoR5/static/**: Static files, including stylesheets and JavaScript files.
- **autoR5/templates/**: HTML templates for the application.
- **requirements.txt**: A list of required Python packages and dependencies.
- **manage.py**: The Django management script for running development servers and managing the project.

## Getting Started

## Requirements

Before running the **autoR5** car rental system, ensure that you have the following Python modules and packages installed. You can use `pip` to install these requirements. The package names are followed by their descriptions:

- **Annotated Types1 (0.6.0)**: Module for annotated type hints.
- **ASGI Reference Server2 (3.7.2)**: ASGI reference server for Django applications.
- **Cloudinary3 (1.36.0)**: A package for handling media files with Cloudinary.
- **Crispy Bootstrap 54 (0.7)**: Integration of Crispy Forms with Bootstrap 5.
- **DJ Database URL5 (0.5.0)**: A package to configure the database via a URL.
- **Django6 (4.2.5)**: The core framework for building web applications.
- **Django Allauth7 (0.57.0)**: For user authentication and registration in Django.
- **Django Bootstrap Datepicker Plus8 (5.0.4)**: Provides datepicker widgets for Django.
- **Django Bootstrap V59 (1.0.11)**: A package for integrating Bootstrap 5 styles with Django.
- **Django Cloudinary Storage10 (0.3.0)**: Used for storing media files on Cloudinary.
- **Django Crispy Forms4 (2.0)**: For rendering forms with Bootstrap styles.
- **GeographicLib**: Geographic library for geospatial calculations.
- **GeoPy**: Python client for geocoding and geolocation services.
- **Gunicorn**: A production-ready WSGI server for running Django applications.
- **OAuthLib**: A framework for building OAuth and OAuth 2.0 providers.
- **Pillow**: Python Imaging Library for image handling.
- **Psycopg2**: A PostgreSQL adapter for Django if you are using PostgreSQL as the database.
- **Pydantic1 (2.4.2)**: A data validation and parsing library.
- **Pydantic Core1 (2.10.1)**: Core functionality for Pydantic.
- **PyJWT**: Python implementation of the JWT (JSON Web Token) standard.
- **Python3 OpenID**: Python 3 implementation of the OpenID identity provider.
- **Requests OAuthlib**: OAuthlib integration for Python Requests.
- **SQLParse**: A non-validating SQL parser.
- **Stripe**: Required for handling payment processing with the Stripe payment gateway.
- **WhiteNoise**: A static file serving library for managing static assets.

To install these requirements, you can use the following command:

```bash
pip install -r requirements.txt
