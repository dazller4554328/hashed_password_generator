import hashlib
import random
import string

def generate_password_from_text(input_text, password_length=16):
    # Step 1: Hash the input text
    hashed_text = hashlib.sha256(input_text.encode()).hexdigest()

    # Step 2: Define a set of characters to use in the password (letters, numbers, symbols)
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"

    # Step 3: Create a password by selecting from the hashed characters
    # Using the hash to select characters randomly but deterministically
    random.seed(hashed_text)  # Seed random with the hash to ensure reproducibility

    # Ensure password is at least the specified length
    password = ''.join(random.choice(characters) for _ in range(password_length))

    return password

if __name__ == "__main__":
    # Get the input word
    input_text = input("Enter the word you want to convert into a password: ")

    # Generate and print the password
    password = generate_password_from_text(input_text, password_length=16)  # Minimum length of 16 characters
    print(f"Generated Password: {password}")
