# Main Imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect
import logging
from urllib.parse import quote_plus

# Routes Import
