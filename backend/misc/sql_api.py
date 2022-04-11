import os
import flask
from flask import app
import flask_sqlalchemy
import flask_praetorian
import flask_cors
from werkzeug.security import generate_password_hash, check_password_hash
from bson.json_util import dumps
#from .api import app 


#Database initialization
db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()

# Initialize flask app for the example
#app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

# A generic user model that might be used by an app powered by flask-praetorian
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

# Initialize the flask-praetorian instance for the app
guard.init_app(app, User)
# Initialize a local database for the example
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
db.init_app(app)
# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)

# Add users for the example
with app.app_context():
    db.create_all()
    if db.session.query(User).filter_by(username='Jagan').count() < 1:
        db.session.add(User(
          username='Jagan',
          password=guard.hash_password('strongpassword'),
          roles='admin'
            ))
    db.session.commit()

class SQLAPI:

    def __init__(self):
        # Add users for the example
        with app.app_context():
            db.create_all()
            if db.session.query(User).filter_by(username='Jagan').count() < 1:
                db.session.add(User(
                username='Jagan',
                password=guard.hash_password('strongpassword'),
                roles='admin'
                    ))
            db.session.commit()

    #@app.route('/api/')
    def home(self):
        return {"Hello": "World"}, 200
    
    def add(self):
        db.insert_one({
            "name": "sagar",
            "password": "mongo"
        })

    def users(self):
        users = db.find()
        resp = dumps(users)
        return resp

    def signup(username,password):
        #Signing a user to the database by a POST request and redirect him to login page
        if db.session.query(User).filter_by(username=username).count() < 1:
            db.session.add(User(
                username=username,
                password=password
                ))
        db.session.commit()
        ret={'message': f'Registered successfully. Welcome {username}'}
        return ret

    def login(self,username,password):
        user = guard.authenticate(username, password)
        ret = {'access_token': guard.encode_jwt_token(user)}
        return ret

    def refresh(old_token):
        new_token = guard.refresh_jwt_token(old_token)
        ret = {'access_token': new_token}
        return ret

    @flask_praetorian.auth_required
    def protected():
        #A protected endpoint. The auth_required decorator will require a header
        #containing a valid JWT
        #.. example::
        #   $ curl http://localhost:5000/api/protected -X GET \
        #     -H "Authorization: Bearer <your_token>"
        return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}

    def to_dict(self, obj):
        if isinstance(obj, dict):
            return obj

        if isinstance(obj, flask_sqlalchemy.engine.RowProxy):
            return {x[0]: x[1] for x in obj.items()}

        raise TypeError(f'Failed to convert {type(obj)} to dict.')

    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'status': 404,
            'message': 'Not Found: ' + flask.request.url,
        }
        resp = flask.jsonify(message)
        resp.status_code = 404

        return resp

# Run the example
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)