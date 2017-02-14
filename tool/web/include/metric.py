from datetime import datetime, timedelta, date
from copy import deepcopy
from collections import OrderedDict, defaultdict, Callable
from flask import render_template, current_app, request
import plotly
import pandas as pd
import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import aliased

from .common.base import BaseView
from .common.function import *
from db import *


def get_current_team_cats_count(cats):
    cat_filter = or_(1==2)
    for cat in cats:
        cat_filter = or_(cat_filter, Issue.category==Category.query.filter_by(c_name=cat).first())

    status_filter = or_(Issue.state==State.query.filter_by(s_name='Ongoing').first(), \
        Issue.state==State.query.filter_by(s_name='New').first())

    ret = Issue.query.filter(and_(status_filter, cat_filter )). \
                        add_columns(func.count(Issue.team_id)).group_by(Issue.team_id).all()
    team_name = []
    team_count = []
    for x, c in ret:
        team_name.append(x.team.g_name)
        team_count.append(c)
    return team_name, team_count


def get_days_cats_team_count(cats, from_date, to_date):
    teams = [x[0] for x in Group.query.filter_by(in_ps=True).with_entities(Group.g_name).all()]
    Group_T = aliased(Issue.team)
    date_filter = and_(Issue.out_date >= from_date, Issue.out_date <= to_date)

    cat_filter = or_(1==2)
    for cat in cats:
        cat_filter = or_(cat_filter, Issue.category==Category.query.filter_by(c_name=cat).first())

    ret = Issue.query.filter(and_(date_filter, cat_filter) ).outerjoin(Group_T, Issue.team).with_entities( \
            Group_T.g_name.label('team'), Issue.out_date).add_columns(func.count(Issue.out_date)).\
                group_by(Issue.out_date, 'team').all()
    res = dict()
    day_cal = (to_date - from_date).days + 1
    for x in teams:
        days = [from_date+timedelta(days=i) for i in range(day_cal)]
        res[x] = OrderedDict(zip(days, [0]*day_cal))
    for team, day, count in ret:
        res[team][day]=count
    counts = []
    for team in teams:
        counts.append(list())
        for day, count in res[team].items():
            counts[-1].append(count)

    return teams, counts


def moving_average(a, n=4) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def get_weeks_cats_team_count(cats, from_date, to_date, mo_avg=False):
    day_cal = (to_date - from_date).days + 1
    week_cal = int(day_cal / 7)
    teams, counts = get_days_cats_team_count(cats, from_date, to_date)
    for t in range(len(teams)):
        tmp_list = []
        for w in range(week_cal):
            tmp_list.append(sum(counts[t][w*7:(w*7+7)]))
        counts[t] = deepcopy(tmp_list)
        if mo_avg:
            counts[t] = list(moving_average(counts[t]))
    return teams, counts


def get_productivity(teams, counts, to_date):
    week_cal = len(counts[0])
    oldest_day = to_date - timedelta(days=(week_cal-1)*7)
    for k, team in enumerate(teams):
        member_json = Group.query.filter_by(g_name=team).with_entities(Group.member).first()[0]
        j = 0
        for i in range(0, week_cal*7, 7):
            tmp_day = oldest_day+timedelta(days=i)
            # print(team, tmp_day, member_json)
            team_count = get_team_member(member_json, tmp_day)
            counts[k][j] /= team_count
            j += 1
    return teams, counts


class OrderedDefaultdict(OrderedDict):
    def __init__(self, default_factory=None, *args, **kwargs):
        if not (default_factory is None
                or isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable or None')
        super(OrderedDefaultdict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key,)
        self[key] = value = self.default_factory()
        return value


def get_weeks_cycle_time(cats, from_date, to_date):
    teams = [x[0] for x in Group.query.filter_by(in_ps=True).with_entities(Group.g_name).all()]
    Group_T = aliased(Issue.team)
    day_cal = (to_date - from_date).days + 1
    week_cal = int(day_cal / 7)
    date_filter = and_(Issue.out_date >= from_date, Issue.out_date <= to_date)

    cat_filter = or_(1==2)
    for cat in cats:
        cat_filter = or_(cat_filter, Issue.category==Category.query.filter_by(c_name=cat).first())

    ret = Issue.query.filter(and_(date_filter, cat_filter) ).outerjoin(Group_T, Issue.team).with_entities( \
            Group_T.g_name.label('team'), Issue.out_date, Issue.in_date).all()

    # assert current_app.debug == False
    res = dict()
    for team in teams:
        days = [from_date+timedelta(days=i) for i in range(day_cal)]
        res[team] = OrderedDict(zip(days, [[] for _ in range(day_cal)]))
    for team, out_day, in_day in ret:
        res[team][out_day].append(in_day)
    counts = []
    for team in teams:
        counts.append(list())
        for outday, in_day_list in res[team].items():
            total_day_count = 0
            total_count = 0
            for one_in_day in in_day_list:
                total_day_count += (outday - one_in_day).days
                total_count += 1
            counts[-1].append((total_count, total_day_count))

    week_counts = []
    for team_counts in counts:
        week_counts.append([])
        for week in range(week_cal):
            count_total_list = list(zip(*team_counts[week*7:week*7+7]))
            week_total_count = sum(count_total_list[1])
            week_count = sum(count_total_list[0])
            week_counts[-1].append(week_total_count/week_count if week_count else 0)

    return teams, week_counts


class MetricView(BaseView):
    def get(self, m_id=None):
        # assert current_app.debug == False
        if m_id is None:
            categories = Category.select()
            return render_template('metric.html', categories=categories)
        else:
            args = dict(request.args)
            from_date = args.pop('from_date')[0] if 'from_date' in args else ''
            to_date = args.pop('to_date')[0] if 'to_date' in args else ''
            cats = list(args.keys())

            if m_id == 1:
                team_name, team_count = get_current_team_cats_count(cats)
                fig = {
                    'data': [{
                        'labels': team_name,
                        'values': team_count,
                        'type': 'pie'
                    }],
                    'layout': {'title': 'LRC New/Ongoing '+' '.join(cats)}
                }
                return get_json(fig), 200

            elif m_id == 2:
                if from_date and to_date:
                    from_date = date(*map(int, from_date.split('-')))
                    to_date = date(*map(int, to_date.split('-')))
                    day_cal = (to_date - from_date).days + 1
                else:
                    to_date = date.today()
                    day_cal = 30
                    from_date = to_date - timedelta(days=day_cal-1)

                teams, counts = get_days_cats_team_count(cats, from_date, to_date)
                x = [str(from_date+timedelta(days=i)) for i in range(day_cal)]

                data = []
                for i in range(len(teams)):
                    data.append({
                        'x':  x,
                        'y': counts[i],
                        'name':  teams[i],
                        'mode':  'lines+markers',
                        'line': {
                            'shape':  'spline'
                        }
                    })
                layout = dict(title = 'Resolved '+' '.join(cats) + '(in 30 days)',
                            xaxis = dict(title = 'Date'),
                            yaxis = dict(title = 'Resolved count'),
                            )
                fig = dict(data=data, layout=layout)
                return get_json(fig), 200

            elif m_id == 3:
                if from_date and to_date:
                    from_date = date(*map(int, from_date.split('-')))
                    to_date = date(*map(int, to_date.split('-')))
                    day_cal = (to_date - from_date).days + 1
                else:
                    to_date = date.today()
                    day_cal = 30
                    from_date = to_date - timedelta(days=day_cal-1)

                teams, counts = get_days_cats_team_count(cats, from_date, to_date)
                x = [str(from_date+timedelta(days=i)) for i in range(day_cal)]

                data = []
                for i in range(len(teams)):
                    data.append({
                        'x' : x,
                        'y' : counts[i],
                        'name' : teams[i],
                        'type': 'bar'
                    })
                layout = dict(title = 'Daily PS/Team relative resolved ' +' '.join(cats),
                            xaxis = dict(title = 'Date'),
                            yaxis = dict(title = 'Resolved count'),
                            barmode = 'relative'
                            )
                fig = dict(data=data, layout=layout)
                return get_json(fig), 200

            elif m_id == 4:
                if to_date:
                    to_date = date(*map(int, to_date.split('-')))
                else:
                    to_date = date.today()
                week_cal = 17
                day_cal = week_cal * 7
                from_date = to_date - timedelta(days=day_cal-1)

                teams, counts = get_weeks_cats_team_count(cats, from_date, to_date, mo_avg=True)
                teams.append('PS Total')

                week_count = len(counts[0])
                ps_total = [0]*week_count
                for team in counts:
                    for i in range(week_count):
                        ps_total[i] += team[i]
                counts.append(ps_total)

                x = []
                for i in range(0, week_cal*7, 7):
                    tmp = (from_date+timedelta(days=i)).isocalendar()[:2]
                    x.append(str(tmp[0])+'-'+str(tmp[1]))

                data = []
                for i in range(len(teams)):
                    data.append({
                        'x': x,
                        'y': counts[i],
                        'name': teams[i],
                        'mode': 'lines+markers',
                        'shape': 'spline',
                        'line': {
                            'shape':  'spline'
                        }
                    })
                layout = dict(title = 'Resolved '+' '.join(cats) + ' (Rolling Average of 4 weeks)',
                            xaxis = dict(title = 'Week'),
                            yaxis = dict(title = 'Resolved count'),
                            )
                fig = dict(data=data, layout=layout)
                return get_json(fig), 200

            elif m_id == 5:
                if to_date:
                    to_date = date(*map(int, to_date.split('-')))
                else:
                    to_date = date.today()
                week_cal = 14
                day_cal = week_cal * 7
                from_date = to_date - timedelta(days=day_cal-1)

                teams, counts = get_weeks_cats_team_count(cats, from_date, to_date)
                teams, counts = get_productivity(teams, counts, to_date)

                x = []
                for i in range(0, week_cal*7, 7):
                    tmp = (from_date+timedelta(days=i)).isocalendar()[:2]
                    x.append(str(tmp[0])+'-'+str(tmp[1]))

                data = []
                for i in range(len(teams)):
                    data.append({
                        'x': x,
                        'y': counts[i],
                        'name': teams[i],
                        'mode': 'lines+markers',
                        'shape': 'spline',
                        'line': {
                            'shape':  'spline'
                        }
                    })
                layout = dict(title = 'Team productivity of '+' '.join(cats),
                            xaxis = dict(title = 'Week'),
                            yaxis = dict(title = 'Productivity'),
                            )
                fig = dict(data=data, layout=layout)
                return get_json(fig), 200

            elif m_id == 6:
                if to_date:
                    to_date = date(*map(int, to_date.split('-')))
                else:
                    to_date = date.today()
                week_cal = 14
                day_cal = week_cal * 7
                from_date = to_date - timedelta(days=day_cal-1)

                teams, counts = get_weeks_cycle_time(cats, from_date, to_date)

                x = []
                for i in range(0, week_cal*7, 7):
                    tmp = (from_date+timedelta(days=i)).isocalendar()[:2]
                    x.append(str(tmp[0])+'-'+str(tmp[1]))

                data = []
                for i in range(len(teams)):
                    data.append({
                        'x': x,
                        'y': counts[i],
                        'name': teams[i],
                        'mode': 'lines+markers',
                        'shape': 'spline',
                        'line': {
                            'shape':  'spline'
                        }
                    })
                layout = dict(title = 'Team Cycle Time of '+' '.join(cats),
                            xaxis = dict(title = 'Week'),
                            yaxis = dict(title = 'Cycle Time (days)'),
                            )
                fig = dict(data=data, layout=layout)
                return get_json(fig), 200
