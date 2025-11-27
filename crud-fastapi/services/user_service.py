from sqlalchemy.orm import Session
from models.user import User
from auth import hash_password, verify_password, create_jwt_token
from fastapi import HTTPException
from logger import logger


class UserService:
    """
    Service layer handling user-related operations such as registration and login.
    Follows clean separation of concerns by keeping business logic outside controllers.
    """

    @staticmethod
    def register_user(user_data, db: Session):
        """
        Register a new user:
        - Checks if username already exists
        - Hashes password before saving
        - Stores new user in the database
        """
        logger.info("Attempting to register new user: %s", user_data.username)

        # Check if the username is already taken
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            logger.warning("Registration failed: username '%s' already exists", user_data.username)
            raise HTTPException(status_code=400, detail="Username already taken")

        # Create user record with hashed password
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password)
        )

        # Commit new user to the database
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info("User registered successfully: %s", new_user.username)
        except Exception as e:
            logger.error("Database error while registering user '%s': %s", user_data.username, str(e))
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to register user")

        return new_user

    @staticmethod
    def login_user(user_data, db: Session):
        """
        Authenticate user:
        - Validates username and password
        - Generates JWT token for successful login
        """
        logger.info("Login attempt for username: %s", user_data.username)

        # Fetch user by username
        db_user = db.query(User).filter(User.username == user_data.username).first()

        # Validate credentials
        if not db_user or not verify_password(user_data.password, db_user.password):
            logger.warning("Invalid login attempt for username: %s", user_data.username)
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Create JWT token
        token = create_jwt_token({"username": db_user.username})
        logger.info("User logged in successfully: %s", db_user.username)

        return {"access_token": token, "token_type": "bearer"}
