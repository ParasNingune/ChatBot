import os
from dotenv import load_dotenv
import warnings
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from faq_handler import get_faq_answer

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
    
    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        user_message = data.get("message", "")
        
        # Get the response from the FAQ handler
        answer = get_faq_answer(user_message)
    
        return jsonify({"answer": answer})
    
    return app