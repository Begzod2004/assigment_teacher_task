from datetime import timedelta

SECRET_KEY = "uhdouasf8yhef8y9hr08fhy8rfh208ru3fh02fh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_EXPIRE_MINUTES = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 