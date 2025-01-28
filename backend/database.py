import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL")
DATABASE_NAME = "novanectar"

class Database:

    def __init__(self):

        """
            Initialize the Database class and set up the MongoDB client and database.
        """

        self.client = None
        self.db = None

    def connect(self):

        """
            Establish a connection to the MongoDB server and select the database.
        """

        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            print(f"Connected to MongoDB: {MONGO_URI}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name):

        """
            Retrieve a specific collection from the database.

            Args:
                collection_name (str): Name of the collection to retrieve.

            Returns:
                Collection: The MongoDB collection object.
        """

        if self.db is None:
            raise Exception("Database connection not initialized. Call connect() first.")
        return self.db[collection_name]

    def close(self):

        """
            Close the MongoDB connection.
        """

        if self.client is not None:
            self.client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    db_instance = Database()
    db_instance.connect()

    try:
        faq_collection = db_instance.get_collection("faq")
        print("FAQ collection accessed successfully.")
    except Exception as e:
        print(f"Error accessing collection: {e}")

    db_instance.close()