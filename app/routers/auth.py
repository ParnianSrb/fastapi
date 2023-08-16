from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    # first find user by Email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # No User with this Email - Let them Guess!!!
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials!')

    # Not the correct Password - Let them Guess!!!
    # Verify the password user sent, which is plain and needs to be compared with the hashed one in the database
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials!')

    # Create Token
    # Return Token

    # Payload (we choose the data, here it is the ID of the user)
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}
