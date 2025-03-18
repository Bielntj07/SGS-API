import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'BF98B4A18A1D173E626F95644FA3A'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sgs.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
