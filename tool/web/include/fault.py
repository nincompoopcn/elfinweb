from flask import request, g

from .common.base import BaseView
from .common.function import *
from db import *

class FaultView(BaseView):
    def get(self, f_id=None):
        if f_id is None:
            faults = Fault.select()

            for i, fault in enumerate(faults):
                faults[i] = fault._asdict()
        
            return get_json(faults), 200
        else:
            filter = and_(Fault.f_id==f_id)
            fault = Fault.select(filter)[0]
            fault_dict = fault._asdict()
            return get_json(fault_dict), 200
    
    def post(self):
        if g.privilege < 1:
            return '', 401

        f_name = request.form['f_name']
        fault_dict = {
            'f_name': f_name
        }

        Fault.insert(fault_dict)
        return '', 200

    def put(self, f_id):
        if g.privilege < 1:
            return '', 401

        f_name = request.form['f_name']
        description = None if request.form['description'] == '' else request.form['description']
        
        fault_dict = {
            'f_name': f_name,
            'description': description
        }
        
        Fault.update(f_id, fault_dict)
        return '', 200

    def delete(self, f_id):
        if g.privilege < 1:
            return '', 401

        Fault.delete(f_id);
        return '', 200