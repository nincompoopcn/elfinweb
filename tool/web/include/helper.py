import os
import shutil
import time
import random
import logging
from werkzeug import secure_filename
from flask import after_this_request, render_template, current_app, request, send_from_directory

import logging
from .common.base import BaseView

JOURNAL_DIR = 'tmp/journal/'

class HelperView(BaseView):
    def get(self):
        return render_template('helper.html')

    def post(self):
        file = request.files['journal-files']
        filename = secure_filename(file.filename)

        time_str = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(time.time()))
        random_str = str(random.randint(100000, 999999))
        folder = JOURNAL_DIR + time_str + random_str
        os.mkdir(folder)

        @after_this_request
        def remove_journal(response):
            shutil.rmtree(folder)
            return response

        try:
            file.save(os.path.join(folder, filename))
        except Exception:
            return '<script type="text/javascript">window.parent.showError();</script>'
        else:
            os.system('journalctl -D %s > %s/journal.log' % (folder, folder))

            path = os.path.join(os.getcwd(), folder)
            return send_from_directory(path, 'journal.log', as_attachment=True)
