# Wanderly

Wanderly is a social media web application focused on sharing travel photos and following other users' travel experiences. Users can upload photos, follow other users, and keep track of their followers and following counts.

## Features

- User Registration and Authentication
- Upload Travel Photos
- Follow and Unfollow Users
- Search for Users
- View and Delete Your Own Photos
- View Followers and Following Counts
- Responsive Navigation Bar with Settings Dropdown

## Technologies Used

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript (jQuery)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/wanderly.git
    cd wanderly
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    python -c "from app import db; db.create_all()"
    ```

5. Run the application:

    ```bash
    python app.py
    ```

6. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

### User Registration

1. Go to the registration page by clicking on the "Register" link on the login page.
2. Fill in your details (first name, last name, email, username, and password) and submit the form to create a new account.

### User Login

1. Go to the login page and enter your username and password.
2. Click on the "Login" button to log into your account.

### Upload Photos

1. Once logged in, navigate to the "Upload a Post" link in the navigation bar.
2. Choose a photo file from your device and click on the "Upload" button.

### Follow/Unfollow Users

1. Use the search bar in the navigation bar to search for other users by their username.
2. Click on the "Follow" button next to a user's name to follow them.
3. If you are already following a user, you can click on the "Unfollow" button to unfollow them.

### View and Delete Photos

1. Go to your account page by clicking on the "My Account" link in the navigation bar.
2. You can view your uploaded photos and delete any photo by clicking on the "Delete" button below the photo.

### Change Username

1. Go to the "Settings" dropdown menu in the navigation bar and click on the "Change Username" link.
2. Enter your new desired username and submit the form to update your username.

## Project Structure

