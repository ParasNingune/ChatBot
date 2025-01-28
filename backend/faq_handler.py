import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URL")

def get_faq_answer(user_query):

    """
        Fetches an FAQ answer from the database based on the user's query.

        Args:
            user_query (str): The user's question/query.

        Returns:
            str: The matching FAQ answer or a fallback message.
    """

    try:
        with MongoClient(MONGO_URI) as client:
            db = client["novanectar"]
            faq_collection = db["faq"]

            result = faq_collection.find_one(
                {"question": {"$regex": user_query, "$options": "i"}}
            )

            if result:
                return result["answer"]
            
            else:
                return "Sorry, I couldn't find an answer. Please contact support."
            
    except Exception as e:
        return f"An error occurred while fetching the FAQ: {str(e)}"
            

if __name__ == "__main__":
    user_question = "HI"
    print(get_faq_answer(user_question))