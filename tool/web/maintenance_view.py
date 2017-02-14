import logging
from logging.handlers import RotatingFileHandler

from config import LOG
from .include.common.function import *
from .include.common.error import *
from .include.common.router import router

def add_config(app):
    app.config['SECRET_KEY'] = 'I LOVE NOKIA AND MY BOSS :)'
    app.config['PERMANENT_SESSION_LIFETIME '] = 86400

def add_log_handler(app):
    if LOG['ENABLE']:
        file_handler = RotatingFileHandler(LOG['FILE'], 
                                           maxBytes=LOG['SIZE'], 
                                           backupCount=LOG['COUNT'])
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

def add_template_function(app):
    app.add_template_global(get_date_delta, 'get_date_delta')
    app.add_template_global(get_team_member, 'get_team_member')
    
def add_error_handler(app):
    app.register_error_handler(404, error_404)
    app.register_error_handler(500, error_500)

def add_router_handler(app):
    for endpoint, view in router.items():
        view_func = view['view'].as_view(endpoint)
        for url, methods in view['url'].items():
            app.add_url_rule(url,
                             view_func=view_func, 
                             methods=methods)



def maintaince_view_init(app):
    add_config(app)
    add_log_handler(app)
    add_template_function(app)
    add_error_handler(app)
    add_router_handler(app)
    