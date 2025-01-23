from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"

def get_faq_answer(user_query):
    client = MongoClient(MONGO_URI)
    db = client["novanectar"]
    faq_collection = db["faq"]

    result = faq_collection.find_one({"question": {"$regex": user_query, "$options": "i"}})

    client.close()

    if result:
        return result["answer"]
    else:
        return "Sorry, I couldn't find an answer. Please contact support."
    
if __name__ == "__main__":
    user_question = "What services does Novanectar offer?"
    print(get_faq_answer(user_question))