from passlib.context import CryptContext

# Set up the CryptContext to use the bcrypt algorithm.
# bcrypt is designed to be slow, which protects against brute-force attacks.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Takes a plain text password and returns a secure hash.
    Use this when a new user registers.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain text password against the hashed version in the database.
    Use this when a user attempts to log in.
    """
    return pwd_context.verify(plain_password, hashed_password)

# ==========================================
# Example Usage (You can delete this part later)
# ==========================================
if __name__ == "__main__":
    # Simulate a user registering
    user_input = "MySuperSecretPassword!"
    secure_hash = get_password_hash(user_input)
    
    print(f"Original: {user_input}")
    print(f"Saved to Database: {secure_hash}")
    
    # Simulate a login attempt
    login_attempt = "MySuperSecretPassword!"
    is_valid = verify_password(login_attempt, secure_hash)
    print(f"Login successful? {is_valid}")