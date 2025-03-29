import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import Firebase configuration and authentication
from firebase_config import firestore_client
from firebase_admin import auth
from google.cloud.firestore_v1 import SERVER_TIMESTAMP  # Correct import for server timestamp

def create_user(email, password, full_name, date_of_birth, phone_number):
    """
    Creates a new user in Firebase Authentication and stores additional data in Firestore.

    :param email: User's email address
    :param password: User's password
    :param full_name: User's full name
    :param date_of_birth: User's date of birth (MM-DD-YYYY format).
    :param phone_number: User's phone number.
    :return: Created user details or error message.
    """
    try:
        # Create the user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f"Successfully created user: {user.uid}")

        # Store additional data in Firestore
        user_data = {
            "email": email,
            "fullName": full_name,
            "dateOfBirth": date_of_birth,
            "phoneNumber": phone_number,
            "uid": user.uid,
            "createdAt": SERVER_TIMESTAMP  # Use correct server timestamp constant
        }
        doc_ref = firestore_client.collection("users").document(user.uid)
        doc_ref.set(user_data)
        print(f"User data stored in Firestore for {user.uid}: {user_data}")

        return user_data
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Example usage with command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python create_account.py <email> <password> <full_name> <date_of_birth> <phone_number>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3]
    date_of_birth = sys.argv[4]  # Expecting MM-DD-YYYY format.
    phone_number = sys.argv[5]

    create_user(email, password, full_name, date_of_birth, phone_number)
