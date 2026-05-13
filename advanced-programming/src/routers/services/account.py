from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import EmailStr
from ..logic import User, UserCreate, UserOut
from ..database import Base

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FHNW domain validation
FHNW_DOMAIN = "students.fhnw.ch"


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its hash.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to compare against
        
    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_email_domain(email: str) -> bool:
    """
    Validate that email belongs to FHNW domain.
    
    Args:
        email (str): The email to validate
        
    Returns:
        bool: True if email is from FHNW domain, False otherwise
    """
    return email.lower().endswith(f"@{FHNW_DOMAIN}")


def create_account(user_data: UserCreate, db: Session) -> UserOut:
    """
    Create a new user account with validation and database persistence.
    
    This function performs the following operations:
    1. Validates that the email is from the FHNW domain (students.fhnw.ch)
    2. Checks if an account with the given email already exists
    3. Hashes the user's password using bcrypt
    4. Creates a new User record in the database
    5. Returns the created user information
    
    Args:
        user_data (UserCreate): Pydantic schema containing:
            - email (EmailStr): Valid email address from FHNW domain
            - password (str): User's password to be hashed
            - university (Optional[str]): University name (default: "FHNW")
            - degree (Optional[str]): Degree program
            - studycourse (Optional[str]): Study course/major
            - interests (Optional[str]): User interests
        db (Session): SQLAlchemy database session
        
    Returns:
        UserOut: Created user object with id, email, and university
        
    Raises:
        HTTPException (422): If email is not from FHNW domain
        HTTPException (400): If email already exists in database
        
    Example:
        >>> from sqlalchemy.orm import Session
        >>> from logic import UserCreate
        >>> user_data = UserCreate(
        ...     email="john.doe@students.fhnw.ch",
        ...     password="secure_password123",
        ...     degree="Computer Science",
        ...     studycourse="Software Engineering"
        ... )
        >>> new_user = create_account(user_data, db)
        >>> print(new_user.email)
        john.doe@students.fhnw.ch
    """
    
    # Validate email domain (only FHNW students)
    if not validate_email_domain(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Email must be from {FHNW_DOMAIN} domain. Only students are allowed to register."
        )
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use login or try another email."
        )
    
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # Create new user instance
    new_user = User(
        email=user_data.email.lower(),  # Store email in lowercase for consistency
        hashed_password=hashed_password,
        university=user_data.university or "FHNW",
        degree=user_data.degree,
        studycourse=user_data.studycourse,
        interests=user_data.interests
    )
    
    # Add to database session and commit
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserOut.from_orm(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the account. Please try again."
        )


def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by their email address.
    
    Args:
        email (str): The email address to search for
        db (Session): SQLAlchemy database session
        
    Returns:
        User: User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email.lower()).first()


def user_exists(email: str, db: Session) -> bool:
    """
    Check if a user account exists for the given email.
    
    Args:
        email (str): The email address to check
        db (Session): SQLAlchemy database session
        
    Returns:
        bool: True if user exists, False otherwise
    """
    return db.query(User).filter(User.email == email.lower()).first() is not None
