
#from api.classes import ReadData
#import pymongo
# from flask_pymongo import PyMongo
#from pymongo.errors import BulkWriteError
from bson.json_util import dumps
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
# import pandas as pd
# from bson.codec_options import CodecOptions
# import pytz
# Initialize flask app for the example
# app.debug = True
# app.config['SECRET_KEY'] = 'top secret'
# app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
# app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
# #app.config["MONGO_URI"] = "mongodb://localhost:27017/cricket_analysis"
# app.config["MONGO_URI"] = "mongodb+srv://jagan-admin:Indial00p$@cluster0.wough.mongodb.net/airbus?retryWrites=true&w=majority"
# #"mongodb+srv://jagan-admin:Indial00ps@cluster0.wough.mongodb.net/cricket_analysis"
# mongodb_client = PyMongo(app)
# #mongodb_client = PyMongo(app, ssl_cert_reqs=ssl.CERT_NONE)
# #print(mongodb_client)
# #Database initialization
# db = mongodb_client.db
# # Initializes CORS so that the api_tool can talk to the example app

import os
import flask
from flask import request, jsonify
import ssl
import json
import flask_cors
from pymongo import MongoClient
# from .api import app

client = MongoClient("mongodb+srv://jagan-admin:Indial00p$@cluster0.wough.mongodb.net/?retryWrites=true&w=majority")
db = client["airbus"]
collection_products = db["products"]
collection_users = db["users"]

cors = flask_cors.CORS()
cors.init_app(app)

class NoSQLAPI:
    #Airbus API
    def getProductsByCat(self, category):
        self.cateogory=category
        print(category)
        cat_data = db.products.find({'product_category':category})
        print(cat_data)
        resp = dumps(cat_data)
        return resp

    def allAirbusProductsData(self):
        all_products_data = db.products.find()
        resp = dumps(all_products_data)
        print(resp)
        return resp

    def addProductNOSQLAPI(self,product):
        resp = db.products.insert_one(product)
        print(resp)

    def updateProductNOSQLAPI(self,product):
        print(product)
        query = {"product_id":product["product_id"]}
        update = { "$set": product}
        resp = db.products.update_one(query,update)
        print(resp)

    def removeProductNOSQLAPI(self,product):
        #delete statement to be added
        myquery = { "product_id": product["product_id"] }
        resp = db.products.delete_one(myquery)
        print(resp)

    def getCategories(self):
        #fetch distinct categories from table
        cat_data = db.products.find().distinct("product_category")
        print(cat_data)
        resp = dumps(cat_data)
        return resp

    def login_check_mongodb(self,username,password):
        login_check = db.users.find({"username":username,"password":password})
        if login_check:
            resp = dumps(login_check)
            return resp
    #End of Airbus API

    def users(self):
        users = db.user_data.find()
        print(users)
        resp = dumps(users)
        return resp

    @app.errorhandler(404)
    def not_found(self,error=None):
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404

        return resp

# Run the example
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)