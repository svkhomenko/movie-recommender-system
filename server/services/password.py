from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def compare_passwords(password: str, original: str):
    return pwd_context.verify(password, original)


def hash_password(password: str):
    return pwd_context.hash(password)
