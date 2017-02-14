import math
from flask import render_template, request, session, g
from flask import current_app

from .common.base import BaseView
from .common.function import *
from config import TABLE
from db import *

class IssueView(BaseView):
    def get(self, i_id=None):
        if i_id is None:
            page = request.args.get('page')
            if page and int(page) > 0: 
                page = int(page) - 1
            else:
                page = 0

            filter = and_(1==1)
            input = {}

            category_list = request.args.getlist('category')
            input['category'] = []
            category_filter = []
            for category in category_list:
                if int(category) > 0:
                    input['category'].append(int(category))
                    category_filter.append(Issue.category_id==int(category))
            filter = and_(filter, or_(*category_filter))

            pronto = request.args.get('pronto')
            if pronto:
                filter = and_(filter, Issue.pronto==pronto)
                input['pronto'] = pronto

            monsho = request.args.get('monsho')
            if monsho:
                filter = and_(filter, Issue.monsho==monsho)
                input['monsho'] = monsho

            title = request.args.get('title')
            if title:
                filter = and_(filter, Issue.title.like('%%%s%%' % title))
                input['title'] = title

            person = request.args.get('person')
            if person:
                filter = and_(filter, Issue.person.like('%%%s%%' % person))
                input['person'] = person

            state_list = request.args.getlist('state')
            input['state'] = []
            state_filter = []
            for state in state_list:
                if int(state) > 0:
                    input['state'].append(int(state))
                    state_filter.append(Issue.state_id==int(state))
            filter = and_(filter, or_(*state_filter))

            team_list = request.args.getlist('team')
            input['team'] = []
            team_filter = []
            for team in team_list:
                if int(team) > 0:
                    input['team'].append(int(team))
                    team_filter.append(Issue.team_id==int(team))
            filter = and_(filter, or_(*team_filter))
            
            pagination = {}
            issue_cout = Issue.count(filter)
            pagination['count'] = math.ceil(issue_cout / TABLE['NUM'])
            pagination['active'] = page + 1

            categories = Category.select()
            groups = Group.select()
            teams = Group.select(and_(Group.in_ps==True))
            areas = Area.select()
            faults = Fault.select()
            states = State.select()
            releases = Release.select()
            issues = Issue.select(
                filter, 
                Issue.i_id.desc(), 
                page * TABLE['NUM'], 
                TABLE['NUM'])

            today = get_date()

            return render_template('issue.html',
                input=input,
                categories=categories,
                groups=groups,
                teams=teams,
                areas=areas,
                faults=faults,
                states=states,
                releases=releases,
                issues=issues,
                pagination=pagination,
                today=today)
        else:
            filter = and_(Issue.i_id==i_id)
            issue = Issue.select(filter, limit=1)[0]
            issue_json = get_json(issue._asdict())
            return issue_json, 200
    
    def post(self):
        issue_dict = {
            'category_id': int(request.form['category']),
            'pronto': None if request.form['pronto'] == '' else request.form['pronto'],
            'monsho': None if request.form['monsho'] == '' else request.form['monsho'],
            'title': request.form['title'],
            'person': request.form['person'],
            'release_id': int(request.form['release']),
            'in_date': request.form['in'],
            'out_date': None if request.form['out'] == '' else request.form['out'],
            'state_id': int(request.form['state']),
            'note': None if request.form['note'] == '' else request.form['note'],
            'team_id': int(request.form['team']),
            'group_id': int(request.form['group']),
            'area_id': None if request.form['area'] == '0' else int(request.form['area']),
            'fault_id': None if request.form['fault'] == '0' else int(request.form['fault']),
            'ongoing_days': None if request.form['ongoing'] == '' else int(request.form['ongoing']),
            'blocked_days': None if request.form['blocked'] == '' else int(request.form['blocked']),
            'rcfound_days': None if request.form['rcfound'] == '' else int(request.form['rcfound']),
            'knife': None if request.form['knife'] == '' else request.form['knife'],
            'in_rft_day': None if request.form['rft'] == '' else request.form['rft'],
            'rft_fcc_day': None if request.form['fcc'] == '' else request.form['fcc'],
            'fcc_closed_day': None if request.form['closed'] == '' else request.form['closed'],
            'u_id': session['UID'] if 'UID' in session else None
        }
        
        if 'UID' in session:
            Issue.insert(issue_dict)
            return '', 200
        else:
            return '', 401

    def put(self, i_id):
        issue_dict = {
            'category_id': int(request.form['category']),
            'pronto': None if request.form['pronto'] == '' else request.form['pronto'],
            'monsho': None if request.form['monsho'] == '' else request.form['monsho'],
            'title': request.form['title'],
            'person': request.form['person'],
            'release_id': int(request.form['release']),
            'in_date': request.form['in'],
            'out_date': None if request.form['out'] == '' else request.form['out'],
            'state_id': int(request.form['state']),
            'note': None if request.form['note'] == '' else request.form['note'],
            'team_id': int(request.form['team']),
            'group_id': int(request.form['group']),
            'area_id': None if request.form['area'] == '0' else int(request.form['area']),
            'fault_id': None if request.form['fault'] == '0' else int(request.form['fault']),
            'ongoing_days': None if request.form['ongoing'] == '' else int(request.form['ongoing']),
            'blocked_days': None if request.form['blocked'] == '' else int(request.form['blocked']),
            'rcfound_days': None if request.form['rcfound'] == '' else int(request.form['rcfound']),
            'knife': None if request.form['knife'] == '' else request.form['knife'],
            'in_rft_day': None if request.form['rft'] == '' else request.form['rft'],
            'rft_fcc_day': None if request.form['fcc'] == '' else request.form['fcc'],
            'fcc_closed_day': None if request.form['closed'] == '' else request.form['closed']
        }

        filter = and_(Issue.i_id==i_id)
        issue = Issue.select(filter, limit=1)[0]
        if issue.u_id is None or 'UID' in session and session['UID'] == issue.u_id or g.privilege > 0:
            Issue.update(i_id, issue_dict)
            return '', 200
        else:
            return '', 401

    def delete(self, i_id):
        filter = and_(Issue.i_id==i_id)
        issue = Issue.select(filter, limit=1)[0]
        if issue.u_id is None or 'UID' in session and session['UID'] == issue.u_id or g.privilege > 0:
            Issue.delete(i_id);
            return '', 200
        else:
            return '', 401