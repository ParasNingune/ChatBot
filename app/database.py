from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"

def initialize_database():
    client = MongoClient(MONGO_URI)
    db = client["novanectar"]
    faq_collection = db["faq"]

    faq_data = [
        {"question": "What should I do if my system crashes?", 
            "answer": "Contact our support team immediately at novanectarservices012024@gmail.com or call our hotline for urgent assistance."},

        {"question": "Do you provide training for employees?", 
            "answer": "Yes, we offer IT training programs tailored to your team’s needs."},

        {"question": "Can you develop custom software solutions?", 
            "answer": "Yes, we specialize in developing custom software tailored to your business requirements."},

        {"question": "How do you approach IT consulting projects?", 
            "answer": "We start with an in-depth analysis of your business needs, followed by strategy development and implementation."},

        {"question": "How can I reach your sales team?", 
            "answer": "You can email novanectarservices012024@gmail.com or call +918979891703 to get in touch with our sales representatives."},

        {"question": "What are your support hours?", 
            "answer": "Our support team is available 24/7 to assist you."}
    ]
    
    faq_collection.insert_many(faq_data)
    print("Sample FAQ added!!")

    client.close()

if __name__ == "__main__":
    initialize_database()