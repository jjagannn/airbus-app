
import logging
from crypt import methods
from distutils.log import debug
from flask import request, Flask, jsonify, make_response
from pymongo import MongoClient
import hashlib
import datetime
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt
from bson.json_util import dumps
from functools import wraps
from os import environ
from flask_swagger_ui import get_swaggerui_blueprint
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

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

SWAGGER_URL="/swagger"
API_URL="../static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={
        "app_name": "Jagans-Python-Flask-RESTAPI"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# app.register_blueprint(api())

@app.route("/api/public", methods=["GET"])
def common():
    return nosql_api.common()

@app.route("/api/auth/register", methods=["POST"])
def register():
    new_user = request.get_json()
    print(new_user)
    logging.warning(new_user)
    return nosql_api.register(new_user)

@app.route("/api/auth/login", methods=["POST"])
def login():
    login_details = request.get_json()
    return nosql_api.login(login_details)

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    return nosql_api.logout()

@app.route("/api/userdata")
@jwt_required(optional=True)
# @verify_token
def userData():
    return nosql_api.userData()

@app.route('/api/deleteProduct/<id>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_user(id):
    return nosql_api.delete_user(id)

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

@app.route('/api/updateProduct', methods=['PUT'])
@jwt_required(optional=True)
def update_product():
    product_data = request.get_json()
    clean_data = {
        "product_id": product_data["id"],
        "product_name": product_data["productName"],
        "product_category": product_data["productCat"],
        "product_description": product_data["productDescr"],
        "units": product_data["units"]
    }
    return nosql_api.update_product(clean_data)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

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

if __name__ == '__main__':
    app.run(debug=True)
