from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password):
    return pwd_context.hash(password)


def verify(plan_password, hased_password):
    return pwd_context.verify(plan_password, hased_password)