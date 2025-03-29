import sys
import os
import requests

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import Firebase configuration
from firebase_config import FIREBASE_WEB_API_KEY

def login_user(email, password):
    """
    Logs in a user using Firebase Authentication REST API.

    :param email: User's email address
    :param password: User's password
    :return: None (prints success or error message to the terminal)
    """
    try:
        # Firebase REST API URL for login
        REST_API_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        # Payload for the REST API request
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        # Send POST request to Firebase REST API
        response = requests.post(
            REST_API_URL,
            params={"key": FIREBASE_WEB_API_KEY},
            json=payload
        )
        response_data = response.json()

        if response.status_code != 200:
            # Handle errors from Firebase API
            error_message = response_data.get("error", {}).get("message", "Login failed")
            print(f"Login failed for {email}: {error_message}")
        else:
            # Successful login
            print(f"Login successful for {email}!")
            print(f"ID Token: {response_data['idToken']}")
            print(f"Refresh Token: {response_data['refreshToken']}")
    except Exception as e:
        print(f"Error during login: {e}")

# Example usage with command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python login.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    login_user(email, password)
