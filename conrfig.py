import os

# Load environment variables
ENCRYPTION_KEY = os.environ.get('APP_ENCRYPTION_KEY')

if not ENCRYPTION_KEY:
    raise EnvironmentError("Please set the APP_ENCRYPTION_KEY environment variable.")

# Other configurations can be added here
