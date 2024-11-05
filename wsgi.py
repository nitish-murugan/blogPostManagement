import sys
import os

project_home = '/home/your_username/graphql'  # Update this to your PythonAnywhere project path
if project_home not in sys.path:
    sys.path.append(project_home)

# Import the app and create it
from website import createApp

# Initialize the app (this is the application that WSGI uses to serve your app)
application = createApp()
