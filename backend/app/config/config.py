import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.urandom(24)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=0.25)  # 15 minutes
    # CACHE_TYPE= 'RedisCache'
    # CACHE_REDIS_URL= 'redis://localhost:6379/3'
    # CACHE_DEFAULT_TIMEOUT= 10