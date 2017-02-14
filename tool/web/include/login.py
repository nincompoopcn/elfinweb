from flask import render_template, redirect, request, session

from .common.base import BaseView
from tool import Auth

class LoginView(BaseView):
    def get(self):
        if 'UID' in session:
            return redirect('/')
        return render_template('login.html')

    def post(self):
        username = request.form['username']
        password = request.form['password']

        auth = Auth(username, password)
        res = auth.sign_in()
        
        if res:
            session['UID'] = username
            session['PWD'] = password
            session.permanent = True
            return '', 200
        else:
            return '', 401