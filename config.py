import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'autorescue123')

    # Priority: DATABASE_URL -> DB_FILE -> default 'autorescue_v2.db'
    db_file = os.environ.get('DB_FILE', 'autorescue_v2.db')
    default_sqlite = f"sqlite:///{db_file}"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_sqlite)

    SQLALCHEMY_TRACK_MODIFICATIONS = False