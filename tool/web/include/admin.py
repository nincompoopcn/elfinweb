from flask import render_template, redirect, g

from .common.base import BaseView
from db import *

class AdminView(BaseView):
    def get(self):
        if g.privilege < 1:
            return redirect('/')

        teams = Group.select(and_(Group.in_ps==True))
        faults = Fault.select()
        users = Privilege.select(and_(Privilege.level<g.privilege))
        return render_template('admin/admin.html',
            teams=teams,
            faults=faults,
            users=users)
