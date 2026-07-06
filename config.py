import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'autorescue123')

    # MySQL Database Configuration for XAMPP
    # Default: localhost:3306, user: root, password: empty
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'autorescue_v2')
    DB_PORT = os.environ.get('DB_PORT', 3306)

    # MySQL Connection String
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }