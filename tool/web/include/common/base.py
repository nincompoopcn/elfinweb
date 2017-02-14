from flask import session, g
from flask.views import MethodView
from db import *

def before_view_init(f):
    def decorator(*args, **kwargs):
        g.privilege = 0
        
        if 'UID' in session:
            u_id = session['UID']
            filter = and_(Privilege.u_id==u_id)
            privilege = Privilege.select(filter)
            if len(privilege) > 0:
                g.privilege = privilege[0].level

        return f(*args, **kwargs)
    return decorator

class BaseView(MethodView):
    decorators = [before_view_init]