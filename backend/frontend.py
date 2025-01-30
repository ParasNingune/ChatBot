"""
    Contains code for all possible routes
"""

from flask import Flask, request, jsonify
from faq_handler import get_faq_answer

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chatbot():

    data = request.get_json()
    user_query = data.get("message", "")

    response = get_faq_answer(user_query)

    return jsonify({"response": response})

