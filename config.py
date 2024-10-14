import os

class Config:
    SECRET_KEY = os.urandom(24)  
    JWT_SECRET_KEY = '123'  
    JWT_ACCESS_TOKEN_EXPIRES = 3600  