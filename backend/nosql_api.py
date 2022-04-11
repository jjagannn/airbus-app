
from bson.json_util import dumps
from os import environ
from pymongo import MongoClient
import hashlib
import datetime
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt  
import os
import flask
from flask import request, jsonify
import ssl
import json
import flask_cors
from pymongo import MongoClient
import logging
# from .api import app

client = MongoClient(environ.get("MONGO_URI"))
db = client["airbus"]
collection_products = db["products"]
collection_users = db["users"]

# cors = flask_cors.CORS()
# cors.init_app(app)

class NoSQLAPI:
    #Airbus API

    def __init__(self):
        pass

    def common(self):
        return jsonify({"message": "Viewing home page"}), 200


    def register(self, new_user):
        new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
        doc = collection_users.find_one({"username":new_user["username"]})
        if not doc:
            collection_users.insert_one(new_user)
            return jsonify({"message": "User created successfully"}), 201
        else:
            return jsonify({"message": "Username already exists"}), 409


    def login(self, login_details):
        user_from_db = collection_users.find_one({"username": login_details["username"]})

        if user_from_db:
            encrypted_password = hashlib.sha256(login_details["password"].encode("utf-8")).hexdigest()
            if encrypted_password == user_from_db["password"]:
                access_token = create_access_token(identity=user_from_db["email"])
                # key = app.config["JWT_SECRET_KEY"]
                # encoded = jwt.encode({"email": user_from_db["username"]}, Private_key, algorithm="RS256")
                # access_token = jwt.encode({'public_id':user_from_db['username'], 'exp': app.config["JWT_ACCESS_TOKEN_EXPIRES"]}, app.config["JWT_SECRET_KEY"])
                # return jsonify(access_token=access_token, username=user_from_db["username"], email=user_from_db["email"]), 200
                return jsonify(access_token=access_token, username=user_from_db["username"], email=user_from_db["email"]), 200

        return jsonify({'msg': 'The username or password is incorrect'}), 401


    def logout(self):
        response = jsonify({"msg": "logout successful"}), 200
        # unset_jwt_cookies(response)
        return response

    def userData(self):
        products_from_db = []
        for x in collection_products.find({},{"_id":0}):
            products_from_db.append(x)
        logging.info(products_from_db)
        if products_from_db:
            return jsonify(table_data=products_from_db), 200
        else:
            return jsonify({"message": "Profile not found"}), 404

    def delete_user(self, id):
        collection_products.delete_one({'product_id': id})
        resp = jsonify('Product deleted successfully!')
        resp.status_code = 200
        return resp

    def update_product(self, clean_data):
        collection_products.update_one({'product_id': id})
        resp = jsonify('Product updated successfully!')
        resp.status_code = 200
        return resp

    def add_product(self, clean_data):
        if (collection_products.find_one({"product_id": clean_data["product_id"]})):
            resp = jsonify('Data already exists with this product id')
            resp.status_code = 409
        else:
            collection_products.insert_one(clean_data)
            resp = jsonify('Product added successfully!')
            resp.status_code = 200
        return resp
