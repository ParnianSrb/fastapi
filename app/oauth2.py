from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
# // import for get_current_user() function
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# // this is the login po's endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY  (You can write anything)
# Algorithm  (Consider number 56.1 picture - sanjeev folder)
# Expiration time

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'  # Header
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    # now, to_encode includes the user's data -Payload- that we want to send to encode and the Expiration Time

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
# -------------------------------------------------------------------------------------


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        # get the id of the token which is being verified
        payload_id: str = payload.get('user_id')
        if payload_id is None:
            raise credential_exception

        # pass this id through the TokenData schema and return it later
        token_data = schemas.TokenData(id=payload_id)

    except JWTError:
        raise credential_exception  # if there is any Error we did not account for

    # token_data is the fetched payload of a token (which is sent by user) that we verified now
    # it is an id as we defined in auth.py/login()
    return token_data
# -------------------------------------------------------------------------------------

# 84 Verify user is Logged In
def get_current_user(token: str = Depends(oauth2_scheme)):
    # // we are going to pass credential_exception into the verify_access_token() function,
    # // for when there is s.th wrong with the *credentials or the *jwt token
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f'Could not validate credentials',
                                          headers={'www-Authenticate': 'Bearer'})  # // just copy this part
    # // return a call to our verify_access_token() function
    return verify_access_token(token, credentials_exception)



