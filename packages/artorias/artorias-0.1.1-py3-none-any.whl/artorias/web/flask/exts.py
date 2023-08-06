from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate(db=db)
cors = CORS()
cache = Cache()
