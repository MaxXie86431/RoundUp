import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import Firebase configuration and authentication
from firebase_config import firestore_client
from firebase_admin import auth
from google.cloud.firestore_v1 import SERVER_TIMESTAMP


def create_user_and_customize(email, password, full_name, date_of_birth, phone_number, additional_data):
    """
    Creates a new user in Firebase Authentication and stores both essential and customization data in Firestore.

    :param email: User's email address.
    :param password: User's password.
    :param full_name: User's full name.
    :param date_of_birth: User's date of birth (MM-DD-YYYY format).
    :param phone_number: User's phone number.
    :param additional_data: Dictionary of optional customization fields.
    :return: None (prints success or error message).
    """
    try:
        # Create the user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f"Successfully created user with UID: {user.uid}")

        # Define all possible categories with default values for customization
        all_categories = {
            "hsGradYear": "",
            "clubsAcademicTeams": "",
            "videoGames": "",
            "hobbies": "",
            "school": "",
            "career": "",
            "classes": "",
            "pets": ""
        }

        # Merge provided customization data with default categories (skipped fields get default values)
        merged_customization_data = {key: additional_data.get(key, value) for key, value in all_categories.items()}

        # Combine essential and customization data into one Firestore document
        user_data = {
            "email": email,
            "fullName": full_name,
            "dateOfBirth": date_of_birth,
            "phoneNumber": phone_number,
            "uid": user.uid,
            "createdAt": SERVER_TIMESTAMP  # Use correct server timestamp constant
        }
        user_data.update(merged_customization_data)  # Add customization data

        # Store combined data in Firestore
        doc_ref = firestore_client.collection("users").document(user.uid)
        doc_ref.set(user_data)
        print(f"User data stored in Firestore for {user.uid}: {user_data}")
    except Exception as e:
        print(f"Error creating user or storing data: {e}")


# Example usage with command-line arguments
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python create_account.py <email> <password> <full_name> <date_of_birth> <phone_number> [<field=value> ...]")
        sys.exit(1)

    # Parse essential information from command-line arguments
    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3]
    date_of_birth = sys.argv[4]  # Expecting MM-DD-YYYY format.
    phone_number = sys.argv[5]

    # Parse additional customization fields from command-line arguments into a dictionary
    additional_data = {}
    for arg in sys.argv[6:]:
        field, value = arg.split("=")
        additional_data[field] = value

    # Create the user and store both essential and customization data
    create_user_and_customize(email, password, full_name, date_of_birth, phone_number, additional_data)
