from .app.models.models import db 
from .app.config.config import Config
from .app.cache import cache

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS





app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

jwt = JWTManager(app)
cache.init_app(app)



CORS(app)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True,
            "Access-Control-Allow-Credentials": True,
        }
    },
)





from .app.resources.authentication.register import *
from .app.resources.authentication.login import *
from .app.resources.parkinglot.user_operations import *
from .app.resources.parkinglot.admin_operations import *

with app.app_context():
    db.create_all()
    user = User.query.filter_by(full_name="admin").first()
    if not user:
        user = User(full_name="admin",email="admin@gmail.com",password_hash=generate_password_hash("admin"),phone=7028539905,address="Thane",pin_code=421302,role="admin")
        db.session.add(user)
        db.session.commit()        


