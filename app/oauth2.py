from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

# This initializes an instance of the OAuth2PasswordBearer class from the fastapi.security module, which is used to define the token endpoint for authentication.
oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'login')


# These are variables that store the secret key, algorithm and expiration time for the JWT access token, which are read from the settings module
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# This is a function that creates a JWT access token.
# It takes in a dictionary data, which contains the user ID and any additional data that needs to be encoded in the token.
# It creates a copy of the data dictionary, adds an expiration time to it, encodes the data using the jwt.encode() function from the jose module, and returns the resulting token.
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

# This is a function that verifies a JWT access token.
# It takes in the token string and a credentials_exception object, which is raised if the token cannot be decoded or if the user ID is missing.
# It uses the jwt.decode() function from the jose module to decode the token using the secret key and algorithm, and retrieves the user ID from the resulting payload.
# If the user ID is missing, it raises the credentials_exception.
# Otherwise, it creates a TokenData object from the user ID and returns it.

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

# This is a function that gets the current user based on the JWT access token.
# It takes in the token string and a database session db, which are obtained from the Depends function using the oauth2_schema and get_db functions respectively.
# It also initializes a credentials_exception object, which is raised if the token is invalid.
# It calls the verify_access_token() function to very the token validity.


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})   
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user