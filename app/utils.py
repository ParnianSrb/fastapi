from passlib.context import CryptContext

# telling passlib the default hashing algorithm or what hashing algorithm do we want to use (here: bcrypt)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)


# getting the raw/attempted password from user_credentials and compare to the hashed_password from database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

