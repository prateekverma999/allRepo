from passlib.context import CryptContext # type: ignore
from Database import model

# # Initialize the password hasher
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  # need to install "pip install argon2_cffi"

# Function to hash a password
def hash(password: str):
    return pwd_context.hash(password)

# Common query filtering function
def apply_filters(query, name, city, published):
    if name:
        query = query.filter(model.Post.name.ilike(f"%{name}%"))
    if city:
        query = query.filter(model.Post.city.ilike(f"%{city}%"))
    if published is not None:
        query = query.filter(model.Post.published == published)
    return query