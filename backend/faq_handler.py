"""
    Contains code for answering the user queries
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URL")
DATABASE_NAME = "novanectar"

class FAQHandler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.faq_collection = self.db["faq"]
        self.questions, self.answers = self.load_faqs()

    def load_faqs(self):

        """
            Load FAQs from MongoDB and store them for NLP processing.
        """

        faqs = list(self.faq_collection.find({}, {"_id": 0, "question": 1, "answer": 1}))
        questions = [faq["question"] for faq in faqs]
        answers = [faq["answer"] for faq in faqs]
        return questions, answers

    def get_faq_answer(self, user_query):

        """
            Find the most relevant FAQ using NLP (TF-IDF + Cosine Similarity).
        """

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.questions + [user_query])
        
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        best_match_index = similarity_scores.argmax()

        if similarity_scores[0, best_match_index] > 0.3:
            return self.answers[best_match_index]
        else:
            return "Sorry, I couldn't find an exact answer. Please contact support."

faq_handler_instance = FAQHandler()

def get_faq_answer(user_query):
    return faq_handler_instance.get_faq_answer(user_query)

if __name__ == "__main__":
    user_question = "What services does NovaNectar offer?"
    print(get_faq_answer(user_question))
