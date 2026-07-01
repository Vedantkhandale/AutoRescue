import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'autorescue123')

    # Prefer DATABASE_URL env var (e.g. for production), otherwise use a local SQLite file
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///autorescue.db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False