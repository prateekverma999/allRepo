from passlib.context import CryptContext # type: ignore

# # Initialize the password hasher
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  # need to install "pip install argon2_cffi"

def hash(password: str):
    return pwd_context.hash(password)