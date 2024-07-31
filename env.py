# import os
 
# # Database configuration
# os.environ['postgres://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/alive_tank_path_776536'] = 'postgresql://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/alive_tank_path_776536'
 
# # Secret key for Flask/Django applications
# os.environ['SECRET_KEY'] = 'your-secret-key'
 
# # Debug mode
# os.environ['DEBUG'] = 'True'
 
# # API key for a third-party service
# os.environ['API_KEY'] = 'your-api-key'

import os
 
os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DEVELOPMENT", "True")
os.environ.setdefault(
    "DB_URL", 'postgresql://postgres:Admin@localhost/books'
)
