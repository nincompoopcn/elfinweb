from flask import render_template, request

from .common.base import BaseView
from .common.function import *
from db import *

class AreaView(BaseView):
    def get(self):
        group = request.args.get('group')
        area_list = None
        if group and int(group) > 0:
            area_list = Area.select(and_(Area.group_id==int(group)))
            for i, area in enumerate(area_list):
                area_list[i] = area._asdict()
        
        if area_list:
            return get_json(area_list), 200
        else:
            return '', 404