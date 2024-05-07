import uuid
import shortuuid
import bcrypt

def generate_uuid():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return str(s)

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt).decode('utf-8')