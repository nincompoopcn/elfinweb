import re
from flask import redirect, session, request

from .common.base import BaseView
from .common.function import *
from tool import ProntoSpider, Spider
from db import *

class ProntoView(BaseView):
    def get(self, p_id):
        spider = ProntoSpider(session['UID'], session['PWD'])
        pronto_dict = spider.collect_one_pronto(p_id)

        pr_group = pronto_dict['group']
        filter = and_(Group.pr_name==pr_group)
        group = Group.select(filter)
        if len(group) > 0:
            pronto_dict['group'] = group[0].g_name

        pr_state = pronto_dict['state']
        if 'New' == pr_state:
            pronto_dict['state'] = 'New'
        elif 'Closed' == pr_state:
            pronto_dict['state'] = 'Closed'
        else:
            pronto_dict['state'] = 'Ongoing'

        pr_person = pronto_dict['person']
        name_list = re.findall(r'(\w+)[, ]', pr_person)
        if 0 != len(name_list):
            pronto_dict['person'] =  name_list[1] + ' ' + name_list[0]
        else:
            pronto_dict['person'] = ''

        return get_json(pronto_dict), 200

class PersonView(BaseView):
    def get(self):
        spider = Spider(session['UID'], session['PWD'])
        p_id = request.args.get('query')
        if request.args.get('is_mine') == '1':
            p_id = session['UID']

        resp = spider.get_page('https://ullink25.emea.nsn-net.net/api/users/?limit=50&fullname=1&q=' + p_id, False)
        return resp, 200