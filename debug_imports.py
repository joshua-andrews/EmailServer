import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import fastapi
    print(f"FastAPI location: {fastapi.__file__}")
except ImportError as e:
    print(f"Error importing fastapi: {e}")

try:
    import pydantic
    print(f"Pydantic location: {pydantic.__file__}")
except ImportError as e:
    print(f"Error importing pydantic: {e}")

try:
    import boto3
    print(f"Boto3 location: {boto3.__file__}")
except ImportError as e:
    print(f"Error importing boto3: {e}")
