from datetime import datetime
from flask import render_template, request, g

from .common.base import BaseView
from .common.function import *
from db import *

class GroupView(BaseView):
    def get(self, g_id=None):
        if g_id is None:
            in_ps = True if request.args.get('ps') == '1' else False
            filter = and_(Group.in_ps==True) if in_ps else True
            groups = Group.select(filter)

            for i, group in enumerate(groups):
                groups[i] = group._asdict()
        
            return get_json(groups), 200
        else:
            filter = and_(Group.g_id==g_id)
            group = Group.select(filter)[0]
            group_dict = group._asdict()
            group_dict['number'] = get_team_member(group.member)
            group_json = get_json(group_dict)
            return group_json, 200

    def put(self, g_id):
        if g.privilege < 1:
            return '', 401

        t_name = request.form['t_name']
        pr_name = None if request.form['pr_name'] == '' else request.form['pr_name']
        description = None if request.form['description'] == '' else request.form['description']
        date = None if request.form['date'] == '' else request.form['date']
        number = None if request.form['number'] == '' else request.form['number']
        
        group_dict = {
            'g_name': t_name,
            'pr_name': pr_name,
            'description': description
        }

        if date != None and number != None:
            delta = datetime.strptime(date, '%Y-%m-%d').isocalendar()
            year = str(delta[0])
            week = str(delta[1])

            filter = and_(Group.g_id==g_id)
            member_json = '{}' if Group.select(filter)[0].member == None else Group.select(filter)[0].member

            member_dict = get_dict(member_json)
            if year in member_dict:
                member_dict[year][week] = int(number)
            else:
                member_dict[year] = {
                    week: int(number)
                }
            group_dict['member'] = get_json(member_dict)
        
        Group.update(g_id, group_dict)
        return '', 200