class Config:
    SECRET_KEY = "autorescue123"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/autorescue_v2"

    SQLALCHEMY_TRACK_MODIFICATIONS = False