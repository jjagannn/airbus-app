
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
# import jwt

# from .nosql_api import NoSQLAPI
# from db import collection_users, collection_products

#Flask app instance creation
app = Flask(__name__,instance_relative_config= True)

#Initialise sql and nosql instances
# nosql_api = NoSQLAPI()

app.config["JWT_SECRET_KEY"] = "amFnYW5za2V5d2l0aHJhbmRvbWRhdGF0b2JlZW5jb2RlZGZvcmpvdGFyZWFsbHlsb25nbG9uZ3N0cmluZ3Rvc2FqZG5zbGtzbGRrbWFzbmZtYW5tbnNhZGttZm5rbHNuZGtsZnNkbGtmbnNkZjQzNGprMjNoajRraDMyajRoMjNqazRoM2prMjMya2wyMzRta2wyM200a2wyM200a2wzMm00bGtrMjNsazNrbDIzNGtsMjNqa2w0MjNrbDQya2wzNGtsMjM0a25ka2xzZm1rbHNkbWZrbHNkZm1sa3M="
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
app.config["JWT_HEADER_TYPE"] = "JWT"
jwt = JWTManager(app)
# Private_key = `-----BEGIN RSA PRIVATE KEY-----
# Proc-Type: 4,ENCRYPTED
# DEK-Info: DES-EDE3-CBC,2167A08A034DA6B4

# HNhofLsj3SgKlusEuALYsUjQqdcnEdVltRmr1O4PZLuHxQ1nvxGTjudoTDKQfesz
# LT/mTLVfUvjrcN2npkwMOfjsrl6/3YwTBEz7/zQ2y1l46+W1jAD9ox26d4E4VuIe
# pkjojAHMxJ5zsYn3phUKJPdQYlGEui5SRfBCUrMcYc83atB1oJdcnH6JFytVIpAp
# vjw/XHSwObVOXVsG0x7RX2qjRJbmyNxRZtSQ0t+QbsOR6R7lVCIU1tg8TRWqypaP
# saLIFcgVrFEwll9ED54jCVSR2PUA9D7cyB8PzzV9hATyNpW38wI/a7awD7t5k20H
# XekfgI4gSqPCLUWero1kNVsiW8NrYrWT1swAu961Ae8b0gFNfW9A+xyBy9qYaK+O
# mEaFsas8rJmntvYqg2N+r+n6DrQX1SmARKke6cDSj7IRVOvCw0L/N79QAGiIPDtI
# xZzNU5w1IT4sICHZDjX4m0OEIbC5AByAWDNnoI5psq+0nKErf1hMkK20USBFMWey
# RV0PqBQQVTOx4/OAGKoURbOlR8qUkFhwk4KA4WznS+fwMszWBe6eaggLKxJM68L2
# aAN0ZgAtVx5NJlvIBdwK4SYaMJraY9lC1E8q1ciKJgb9WBv0hpkmGNtx6KcMRB2X
# KnlkJ15igZ2mLIc/JpqdBX1wS03TV1mKybRqfCBgSZGK8MiOT/I0pROjgi9G6w5Y
# nFhkZImWLJp7c5lx+S2eft5oHnHpA3VKh0ExyDoTDIxXZhzVKV7a99Ln6VJANeTu
# mVtTsLf9v1WRqz7UYj6YB6u6ZPxJtFq/5bsa9H4BNO6+A2zZGMSAz3pKUshy3W24
# rBk2Hda0PEEzE/7Vk6M69XOGulZbam+0nCLF5SG0rky7w9dXs4VXk0s3coCWEWMm
# yyNWbS07fSSuMOi65RhzouzkYaCYERiZ6PmMmJbicLTAzI1QXQWgh/z8ahkufBV8
# ugK1oR0Angf13efR4SW0Lf3jIVdutiygcFgCsuK2FYHFBxNJkzrDZiudnuA0Htpi
# TCKPNeEfLPwXhhIYZN4C/hNf1MmGVmIGMihA3j1NmJJxyCwlTv77QqvZWKOnjy8t
# DuLjpeVsIRDTgegCvuAZTX7gk+J5YyFdPNj/lrU0AO7onRG46eZo1XXkrRvwZcT/
# OPkU1vjIiQrc4rUi8foTW1+0YYaoyakd+OOIKxVovQR7eNuxck+Ad3FBm7f4M/gB
# 595iDlIvjope0rIGZLt5F2gz1qoGvODghiMuZJlPOsO2ojClPH6SNAerZ1R7Pj19
# Q0RwjLPPMNZ7a6reVyqysK3GtDLOA1Dff7bMMybons3VyWsna5dHvoohwfS+jpTM
# POAdbGwB8eXQQHIDQm2He50Z/m4STcl4xRz9fIT4f2XV8Z8UFAU+zMLFb+coMwHc
# QACQCRZZ3wwGaQE4Th8OpMBghJEVL7uVNEHZXVa6yu7cSddmzZiqHcVjqzdFQpW8
# l2O679vR/d8Ubl2Mqh33W5dslw3FjREwM1Kz04hoNS4Far3PXqe5QT3zK9guK8YV
# 7bx1pRy7wqvcE3NPbZALu/mBtFKcuCJihooZMu6fu7hxNXO6YS26oQ==
# -----END RSA PRIVATE KEY-----`;

# Public_key = `-----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApRQrtXDQ/r3fAl0Oi4zI
# 6um0MoyfbK2vkWZ3/A5nrdRlHgozkma3G8StgmJHC0yKk6HCg2ZiOuJdguWSZWsn
# KJfpkVvKkx8nmgCtm7BuYMwyZwctF0lGaET7XAi7e5YZ2pxnZojstHORO9/ocpXm
# utI08+q+yNlXdTuFBmGB5jTasnalcfwCFnFtKBNi+tzRQi6R39KquGNMFqyhLvCl
# Qhp4V1XMKNyEppDLnG7S9PEMzN+90c4P3uL2sYsBooBxeIeC+cAKngzGARocVrB9
# Ocs7NP1GJ3mlZASO01QtLeFcHO/IV96V+X2HxsrkF6zUbu7K7+/oPCpTF2bqNAje
# EQIDAQAB
# -----END PUBLIC KEY-----`;
# Public_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3RAeWFob28uY29tIn0.Nj3MdNruWAcIcp0iMMBErzFNNCOUcgtH1Kzi8ijD3As"
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
# app.config["JWT_HEADER_TYPE"] = "JWT"
# jwt = JWTManager(app)

client = MongoClient("mongodb+srv://jagan-admin:Indial00p$@cluster0.wough.mongodb.net/?retryWrites=true&w=majority")
db = client["airbus"]
collection_products = db["products"]
collection_users = db["users"]

@app.route("/api/public", methods=["GET"])
def common():
    return jsonify({"message": "Viewing home page"}), 200

@app.route("/api/auth/register", methods=["POST"])
def register():
    new_user = request.get_json()
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
    doc = collection_users.find_one({"username":new_user["username"]})
    if not doc:
        collection_users.insert_one(new_user)
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"message": "Username already exists"}), 409

@app.route("/api/auth/login", methods=["POST"])
def login():
    login_details = request.get_json()
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

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"}), 200
    # unset_jwt_cookies(response)
    return response

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
    products_from_db = []
    for x in collection_products.find({},{"_id":0}):
        products_from_db.append(x)
    logging.info(products_from_db)
    if products_from_db:
        return jsonify(table_data=products_from_db), 200
    else:
        return jsonify({"message": "Profile not found"}), 404

@app.route('/api/deleteProduct/<id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user(id):
	collection_products.delete_one({'product_id': id})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp

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
    if (collection_products.find_one({"product_id": clean_data["product_id"]})):
        resp = jsonify('Data already exists with this product id')
        resp.status_code = 409
    else:
        collection_products.insert_one(clean_data)
        resp = jsonify('Product added successfully!')
        resp.status_code = 200
    return resp

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
