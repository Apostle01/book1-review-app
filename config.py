import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60'
    SQLALCHEMY_DATABASE_URI = os.environ['postgres://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/alive_tank_path_776536'] = 'postgresql://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/alive_tank_path_776536'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    os.environ['DEBUG'] = 'True'