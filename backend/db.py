from pymongo import MongoClient

client = MongoClient("mongodb+srv://jagan-admin:Indial00p$@cluster0.wough.mongodb.net/?retryWrites=true&w=majority")
db = client["airbus"]
collection_products = db["products"]
collection_users = db["users"]