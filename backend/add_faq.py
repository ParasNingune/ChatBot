"""
    Contains code for adding faq, deleting duplicate faq and creating a csv file from the available data
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import csv

load_dotenv()
csv_filename = "faq_data.csv"

MONGO_URI = os.getenv("MONGO_URL")
DATABASE_NAME = "novanectar"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
faq_collection = db["faq"]

faqs = [
    # Greetings
    { "question": "Hello", "answer": "Hello! How can I assist you today?" },
    { "question": "Hi", "answer": "Hi there! How may I help you?" },
    { "question": "Hey", "answer": "Hey! What can I do for you today?" },
    { "question": "Good morning", "answer": "Good morning! How can I help?" },
    { "question": "Good afternoon", "answer": "Good afternoon! What do you need assistance with?" },
    { "question": "Good evening", "answer": "Good evening! How may I assist you today?" },
    { "question": "Good night", "answer": "Good night! Feel free to ask me anything before you go." },
    { "question": "How are you?", "answer": "I'm just a chatbot, but I'm always here to help!" },
    { "question": "What's up?", "answer": "Not much! Just here to assist you. How can I help?" },
    { "question": "Who are you?", "answer": "I'm NovaNectar's chatbot, here to help you with your queries!" },

    # Company Information
    { "question": "What is NovaNectar?", "answer": "NovaNectar is an IT Services and Consulting company specializing in AI, cloud solutions, and software development." },
    { "question": "Where is NovaNectar located?", "answer": "NovaNectar is based in [Your Location], but we provide global services remotely." },
    { "question": "How can I contact NovaNectar?", "answer": "You can reach us at support@novanectar.com or call us at +1-234-567-890." },
    { "question": "When was NovaNectar founded?", "answer": "NovaNectar was founded in [Year] to provide innovative IT solutions." },
    { "question": "What industries do you serve?", "answer": "We work with industries like healthcare, finance, e-commerce, and more." },
    
    # Services
    { "question": "What services do you offer?", "answer": "We offer AI solutions, cloud computing, mobile and web development, and IT consulting." },
    { "question": "Do you provide AI development?", "answer": "Yes, we develop AI models, chatbots, and recommendation systems." },
    { "question": "Can you build mobile apps?", "answer": "Yes, we create iOS and Android apps using React Native and Flutter." },
    { "question": "Do you offer cloud migration?", "answer": "Yes, we provide cloud migration services for AWS, Google Cloud, and Azure." },
    { "question": "Do you provide API development?", "answer": "Yes, we develop REST and GraphQL APIs for seamless integration." },
    { "question": "Can you integrate AI into my website?", "answer": "Absolutely! We can integrate AI chatbots, recommendation systems, and more into your site." },
    
    # Security & Compliance
    { "question": "Is my data secure with NovaNectar?", "answer": "Yes, we follow industry best practices and use encryption to keep your data safe." },
    { "question": "Do you comply with GDPR?", "answer": "Yes, we ensure GDPR compliance for all our services." },
    { "question": "Do you provide cybersecurity services?", "answer": "Yes, we offer penetration testing, vulnerability assessments, and more." },

    # Pricing & Payments
    { "question": "How much do your services cost?", "answer": "Our pricing depends on the project. Contact us for a custom quote!" },
    { "question": "Do you offer free consultations?", "answer": "Yes! We provide free initial consultations to understand your requirements." },
    { "question": "What payment methods do you accept?", "answer": "We accept credit/debit cards, PayPal, and bank transfers." },
    { "question": "Do you have any discounts?", "answer": "We occasionally offer discounts on long-term projects. Contact us for details!" },

    # Technical Questions
    { "question": "What programming languages do you use?", "answer": "We specialize in Python, JavaScript, Java, C++, and more." },
    { "question": "What frameworks do you work with?", "answer": "We use React, Angular, Node.js, Flask, Django, and many more!" },
    { "question": "Do you work with machine learning?", "answer": "Yes! We build machine learning models for various applications." },
    { "question": "Can you develop blockchain applications?", "answer": "Yes, we provide blockchain development services, including smart contracts." },

    # Account & Support
    { "question": "How do I create an account?", "answer": "You can sign up on our website by clicking the 'Register' button and filling in your details." },
    { "question": "I forgot my password", "answer": "You can reset your password by clicking 'Forgot Password' on the login page." },
    { "question": "Do you provide 24/7 support?", "answer": "Yes, NovaNectar offers 24/7 customer support to assist you anytime." },
    
    # Hiring & Careers
    { "question": "Are you hiring?", "answer": "Yes! Check our Careers page for job openings at NovaNectar." },
    { "question": "How can I apply for a job?", "answer": "You can apply by sending your resume to careers@novanectar.com." },
    { "question": "Do you offer internships?", "answer": "Yes, we have internship programs. Contact us for details!" },

    # Random/Fun Questions
    { "question": "Tell me a joke", "answer": "Sure! Why don't programmers like nature? Because it has too many bugs!" },
    { "question": "Who is your creator?", "answer": "I was created by the developers at NovaNectar to assist users like you!" },
    { "question": "What is AI?", "answer": "AI, or Artificial Intelligence, is a branch of computer science that enables machines to learn and make decisions." },
    { "question": "What is the meaning of life?", "answer": "That's a deep question! But I'm here to help with IT-related queries. 😉" },
    
    # Custom User Queries
    { "question": "How long does a project take?", "answer": "Project timelines vary based on complexity. Contact us for an estimate!" },
    { "question": "Do you offer training services?", "answer": "Yes, we provide IT training in various domains." },
    { "question": "Can you develop e-commerce platforms?", "answer": "Yes! We create feature-rich e-commerce solutions tailored to your needs." },
    
    # Chatbot-Specific
    { "question": "How do I use this chatbot?", "answer": "Simply type your question, and I'll do my best to assist you!" },
    { "question": "Can you understand different languages?", "answer": "Currently, I primarily understand English, but multi-language support is coming soon!" },
    { "question": "Are you human?", "answer": "No, I'm an AI chatbot built to assist you with your questions!" }
]

def remove_duplicates():
    seen_questions = set()
    duplicates = []

    for faq in faq_collection.find():
        question = faq["question"].strip().lower()
        if question in seen_questions:
            duplicates.append(faq["_id"])
        else:
            seen_questions.add(question)

    if duplicates:
        faq_collection.delete_many({"_id": {"$in": duplicates}})
        print(f"Removed {len(duplicates)} duplicate FAQ entries.")
    else:
        print("No duplicate entries found.")


def convert_to_csv():
    faqs = list(faq_collection.find({}, {"_id": 0, "question": 1, "answer": 1}))

    if not faqs:
        print("No data found in the FAQ collection.")
        return

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["question", "answer"])
        writer.writeheader()
        writer.writerows(faqs)

    print(f"✅ FAQ data successfully exported to {csv_filename}")

#faq_collection.insert_many(faqs)
print("FAQs inserted successfully!")

#remove_duplicates()

convert_to_csv()