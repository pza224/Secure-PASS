import random
import string

def generate_password(length=50):
    """Generates a secure password with uppercase, lowercase, numbers, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
