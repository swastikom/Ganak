# Main Imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect
import logging
from urllib.parse import quote_plus

# Routes Import
from routes.user import router as user_router

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI components from environment variables
username = quote_plus(os.getenv("MONGODB_USER"))
password = quote_plus(os.getenv("MONGODB_PASSWORD"))
host = os.getenv("MONGODB_HOST")
app_name = os.getenv("MONGODB_APP_NAME")

# Construct the URI
MONGODB_URI = f"mongodb+srv://{username}:{password}@{host}/?appName={app_name}"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": "User CRUD Routes",
        "description": "Operations with users. Such as - **Create** a new User, **Read** the information of current authenticated suer, **Update** Update the information of current authenticated user except password, **Delete** the current authenticated user.",
    },
    {
        "name": "User Authentication Routes",
        "description": "Authentication of user with email and password and generation of token to access the protected routes."
    },
    {
        "name": "Password Reset Routes",
        "description": "Firstly give the registered Email where the OTP will go. Then from there get the OTP and set new password."
    }
]

app = FastAPI(openapi_tags=tags_metadata)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    # Connect to MongoDB with a default connection name
    connect(alias='default', host=MONGODB_URI)
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")

# Include the user router
app.include_router(user_router)


