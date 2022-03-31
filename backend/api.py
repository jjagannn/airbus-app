
import logging
from crypt import methods
from distutils.log import debug
from flask import request, Flask, jsonify
from pymongo import MongoClient
import hashlib
import datetime
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt
from bson.json_util import dumps
from functools import wraps
from os import environ
# import jwt
from .nosql_api import NoSQLAPI

#Flask app instance creation
app = Flask(__name__,instance_relative_config= True)
# app.config.from_pyfile('settings.py')

#Initialise sql and nosql instances
nosql_api = NoSQLAPI()
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
app.config["JWT_HEADER_TYPE"] = "JWT"
# jwt = JWTManager(app)

client = MongoClient(environ.get("MONGO_URI"))
db = client["airbus"]
collection_products = db["products"]
collection_users = db["users"]

@app.route("/api/public", methods=["GET"])
def common():
    return nosql_api.common()
    # return jsonify({"message": "Viewing home page"}), 200

@app.route("/api/auth/register", methods=["POST"])
def register():
    new_user = request.get_json()
    return nosql_api.register(new_user)
    # new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
    # doc = collection_users.find_one({"username":new_user["username"]})
    # if not doc:
    #     collection_users.insert_one(new_user)
    #     return jsonify({"message": "User created successfully"}), 201
    # else:
    #     return jsonify({"message": "Username already exists"}), 409

@app.route("/api/auth/login", methods=["POST"])
def login():
    login_details = request.get_json()
    return nosql_api.login(login_details)

    # user_from_db = collection_users.find_one({"username": login_details["username"]})

    # if user_from_db:
    #     encrypted_password = hashlib.sha256(login_details["password"].encode("utf-8")).hexdigest()
    #     if encrypted_password == user_from_db["password"]:
    #         access_token = create_access_token(identity=user_from_db["email"])
    #         # key = app.config["JWT_SECRET_KEY"]
    #         # encoded = jwt.encode({"email": user_from_db["username"]}, Private_key, algorithm="RS256")
    #         # access_token = jwt.encode({'public_id':user_from_db['username'], 'exp': app.config["JWT_ACCESS_TOKEN_EXPIRES"]}, app.config["JWT_SECRET_KEY"])
    #         # return jsonify(access_token=access_token, username=user_from_db["username"], email=user_from_db["email"]), 200
    #         return jsonify(access_token=access_token, username=user_from_db["username"], email=user_from_db["email"]), 200

    # return jsonify({'msg': 'The username or password is incorrect'}), 401

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    # response = jsonify({"msg": "logout successful"}), 200
    # unset_jwt_cookies(response)
    # return response
    return nosql_api.logout()

# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             data = response.get_json()
#             if type(data) is dict:
#                 data["access_token"] = access_token 
#                 response.data = json.dumps(data)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response

# def verify_token(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         token = request.headers.get('Authorization')
        
#         if not token:
#             return jsonify({'message' : 'Token is missing !!'}), 401
#         try:
#             # decoding the payload to fetch the stored details
#             # signing_key = jwks_client.get_signing_key_from_jwt(token)
#             # print(signing_key)
#             data = jwt.decode(token, Public_key, algorithms="RS256")
#             # current_user = data['public_id']
#             # print(data)
#         except:
#             return jsonify({
#                 'message' : 'Token is invalid !!'
#             }), 401
#         return  f(current_user, *args, **kwargs)
#     return wrapper

@app.route("/api/userdata")
@jwt_required(optional=True)
# @verify_token
def userData():
    # current_user = get_jwt_identity()
    # print(current_user)
    return nosql_api.userData()
    # products_from_db = []
    # for x in collection_products.find({},{"_id":0}):
    #     products_from_db.append(x)
    # logging.info(products_from_db)
    # if products_from_db:
    #     return jsonify(table_data=products_from_db), 200
    # else:
    #     return jsonify({"message": "Profile not found"}), 404

@app.route('/api/deleteProduct/<id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user(id):
    return nosql_api.delete_user(id)
	# collection_products.delete_one({'product_id': id})
	# resp = jsonify('User deleted successfully!')
	# resp.status_code = 200
	# return resp

@app.route('/api/addProduct', methods=['POST'])
@jwt_required(optional=True)
def add_product():
    product_data = request.get_json()
    clean_data = {
        "product_id": product_data["id"],
        "product_name": product_data["productName"],
        "product_category": product_data["productCat"],
        "product_description": product_data["productDescr"],
        "units": product_data["units"]
    }
    return nosql_api.add_product(clean_data)
    # if (collection_products.find_one({"product_id": clean_data["product_id"]})):
    #     resp = jsonify('Data already exists with this product id')
    #     resp.status_code = 409
    # else:
    #     collection_products.insert_one(clean_data)
    #     resp = jsonify('Product added successfully!')
    #     resp.status_code = 200
    # return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.run(debug=True)
