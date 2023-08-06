import string
import random

def generate_password(length=12):
  
    characters = string.ascii_letters + string.digits + string.punctuation

  
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
import random
import string

def generate_password():
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits

    # Define the pool of characters to choose from
    pool = lowercase_letters + uppercase_letters + digits


    password = random.choice(lowercase_letters) + random.choice(uppercase_letters) + random.choice(digits)

    # Generate the remaining characters of the password
    remaining_length = 12 - len(password)
    for _ in range(remaining_length):
        password += random.choice(pool)

    # Shuffle the characters in the password to randomize the order
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

# Generate and print a password
password = generate_password()
print(password)
