#exts.py 解决循环引用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_redis import FlaskRedis
import redis
db = SQLAlchemy()
mail = Mail()
redis_client = FlaskRedis()
