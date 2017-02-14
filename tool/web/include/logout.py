from flask import redirect, session

from .common.base import BaseView

class LogoutView(BaseView):
    def get(self):
        session.clear()
        return redirect('/')