from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from config import DB

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def count(cls, db_filter=True):
        return cls.query.filter(db_filter).count()

def maintaince_db_init(app, commit_on_teardown=False):
    db_url = "mysql+pymysql://%s:%s@%s/%s" % (DB['USER'], DB['PASS'], DB['URL'], DB['NAME'])

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = commit_on_teardown

    db.init_app(app)
    # DANGEROUS DO NOT OPEN THIS COMMENT IN PRODUCTION ENVIRONMENT !!!
    # with app.app_context():
    #     from .category import Category
    #     from .release import Release
    #     from .group import Group
    #     from .area import Area
    #     from .state import State
    #     from .issue import Issue
    #     from .privilege import Privilege
    #     db.drop_all()
    #     db.create_all()
    #     Privilege.insert_fake_privilege()
    #     Category.insert_fake_category()
    #     Release.insert_fake_release()
    #     State.insert_fake_states()
    #     Group.insert_fake_group()
    #     Area.insert_fake_area()
    #     Issue.insert_fake_issues(1200)

def commit():
    db.session.commit()
