from flask import render_template, current_app

def error_404(error):
    current_app.logger.error(error)
    return render_template('404.html'), 404

def error_500(error):
    current_app.logger.error(error)
    return '500', 500
