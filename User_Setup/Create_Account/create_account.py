import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import Firebase configuration and authentication
from firebase_config import firestore_client
from firebase_admin import auth

def create_user(email, password):
    """
    Creates a new user in Firebase Authentication.

    :param email: User's email address
    :param password: User's password
    :return: Created user details or error message
    """
    try:
        # Directly use Firebase Admin SDK (already initialized in firebase_config.py)
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f"Successfully created user: {user.uid}")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Example usage with command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_account.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    create_user(email, password)
