import os
from dotenv import load_dotenv
import warnings
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

warnings.filterwarnings("ignore")

load_dotenv()

def create_app():
    app = Flask(__name__)

    CORS(app)

    client = MongoClient(os.getenv("MONGO_URL"))
    app.db = client["novanectar"]

    @app.route('/')
    def home():
        return "Chatbot Backend is running..."
    
    return app