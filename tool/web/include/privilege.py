from flask import render_template, request, g

from .common.base import BaseView
from .common.function import *
from db import *

class PrivilegeView(BaseView):
    def get(self):
        privileges = Privilege.select(and_(Privilege.level<g.privilege))

        for i, privilege in enumerate(privileges):
            privileges[i] = privilege._asdict()
    
        return get_json(privileges), 200

    def post(self):
        if g.privilege < 9:
            return '', 401

        u_id = request.form['u_id']
        privilege_dict = {
            'u_id': u_id,
            'level': 1
        }

        Privilege.insert(privilege_dict)
        return '', 200

    def delete(self, u_id):
        if g.privilege < 9:
            return '', 401

        Privilege.delete(u_id);
        return '', 200