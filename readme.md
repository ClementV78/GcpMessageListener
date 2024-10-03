# Gcp message Listener

## Overview

This project subscribes to a Google Cloud Pub/Sub topic that receives Gmail messages for appointments. It extracts appointment information from these messages and saves it in a database. A scheduler then sends a confirmation SMS to the customer if the appointment is within a specified number of hours.

## Project Structure

## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Copy `.env.example` to [`.env`](".env") and update the values as needed.

## Usage

- **Run the main script:**
    ```sh
    python main.py
    ```

- **Run tests:**
    ```sh
    python -m unittest discover tests
  ```

### Main Components

1. **Database Management ([`db_manager.py`](db_manager.py)):**
    - Handles all database operations including CRUD operations.
    - Uses SQLAlchemy for ORM and database interactions.

2. **Event Handling ([`event_handler.py`](event_handler.py)):**
    - Manages events and triggers appropriate actions.
    - Listens for specific events and processes them accordingly.

3. **Message Scheduling ([`scheduler.py`](scheduler.py)):**
    - Schedules messages to be sent at specific times.
    - Uses APScheduler for scheduling tasks.

4. **SMS Handling ([`sms_handler.py`](sms_handler.py)):**
    - Manages sending and receiving SMS messages.
    - Integrates with external SMS APIs for message delivery.

5. **Google Cloud Pub/Sub Listener ([`pubsub_listener.py`](pubsub_listener.py)):**
    - Listens to messages from Google Cloud Pub/Sub.
    - Processes incoming messages and triggers appropriate actions.


## Key Files

- **[`main.py`]("main.py"):** Entry point of the application.
- **[`config/settings.py`](config/settings.py):** Configuration settings.
- **[`db_manager.py`](db_manager.py):** Database management functions.
- **[`event_handler.py`](event_handler.py):** Event handling logic.
- **[`scheduler.py`](scheduler.py):** Scheduling tasks.
- **[`sms_handler.py`](sms_handler.py):** SMS handling functions.
- **[`tests/test_main.py`](tests/test_main.py):** Unit tests for the main script.

## License

This project is licensed under the MIT License. See the LICENSE file for details.