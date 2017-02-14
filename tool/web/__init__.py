from flask import Flask

from db import maintaince_db_init
from .maintenance_view import maintaince_view_init

app = Flask(__name__)

maintaince_db_init(app)
maintaince_view_init(app)