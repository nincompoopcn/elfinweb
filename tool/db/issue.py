from datetime import datetime
from sqlalchemy.orm import aliased

from .maintenance_db import db, BaseModel
from .category import Category
from .release import Release
from .group import Group
from .area import Area
from .fault import Fault
from .state import State

class Issue(BaseModel):
    __tablename__ = 'issues'
    i_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.c_id'), nullable=False)
    pronto = db.Column(db.Unicode(20))
    monsho = db.Column(db.Unicode(20))
    title = db.Column(db.Unicode(400), nullable=False)
    person = db.Column(db.Unicode(50), nullable=False)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.r_id'), nullable=False)
    in_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    out_date = db.Column(db.Date)
    state_id = db.Column(db.Integer, db.ForeignKey('states.s_id'), nullable=False)
    note = db.Column(db.UnicodeText)
    team_id = db.Column(db.Integer, db.ForeignKey('groups.g_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.g_id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.a_id'))
    fault_id = db.Column(db.Integer, db.ForeignKey('faults.f_id'))
    ongoing_days = db.Column(db.Integer, default=0)
    blocked_days = db.Column(db.Integer, default=0)
    rcfound_days = db.Column(db.Integer, default=0)
    knife = db.Column(db.Unicode(200))
    in_rft_day = db.Column(db.Date)
    rft_fcc_day = db.Column(db.Date)
    fcc_closed_day = db.Column(db.Date)
    u_id = db.Column(db.Unicode(20))

    category = db.relationship('Category', foreign_keys=category_id)
    release = db.relationship('Release', foreign_keys=release_id)
    state = db.relationship('State', foreign_keys=state_id)
    team = db.relationship('Group', foreign_keys=team_id)
    group = db.relationship('Group', foreign_keys=group_id)
    area = db.relationship('Area', foreign_keys=area_id)
    fault = db.relationship('Fault', foreign_keys=fault_id)

    @staticmethod
    def insert_fake_issues(num=0):
        from  sqlalchemy.sql.expression import func, select
        from random import randint
        from datetime import timedelta
        import forgery_py
        from forgery_py import forgery
        for i in range(num):
            area = None
            team = None
            group = Group.query.offset(randint(0, Group.query.count()-1)).first()
            if group.in_ps:
                area = Area.query.filter_by(group_id=group.g_id).order_by(func.rand()).first()
                team = group
            else:
                team = Group.query.filter_by(in_ps=True).order_by(func.rand()).first()
            in_date = forgery.date.date(past=True, min_delta=0, max_delta=180)
            out_date = in_date + timedelta(days=randint(0, 100))
            tmp_dict = {
                        "category" : Category.query.offset(randint(0, Category.query.count()-1)).first(),
                        "pronto" : "PR"+str(randint(10000, 99999)),
                        "monsho" : "M"+str(randint(100, 999)),
                        "title" : forgery_py.lorem_ipsum.sentence(),
                        "person" : forgery.name.full_name(),
                        "release" : Release.query.offset(randint(0, Release.query.count()-1)).first(),
                        "in_date" : in_date,
                        "out_date" : out_date,
                        "state" : State.query.offset(randint(0, State.query.count()-1)).first(),
                        "group" : group,
                        "u_id" : randint(1, 3)
            }
            if area:
                tmp_dict['area'] = area
            if team:
                tmp_dict['team'] = team
            new_issue = Issue(**tmp_dict)
            db.session.add(new_issue)
        db.session.commit()

    def __repr__(self):
        return '<Issue %r>' % self.title

    @staticmethod
    def select(db_filter=True, order_by=None, offset=0, limit=20):
        Group_T = aliased(Issue.team)
        Group_G = aliased(Issue.group)
        ret_col =  [
            Issue.i_id,
            Issue.category_id.label('c_id'),
            Category.c_name.label('category'),
            Issue.pronto,
            Issue.monsho,
            Issue.title,
            Issue.person,
            Issue.release_id.label('r_id'),
            Release.r_name.label('release'),
            Issue.in_date,
            Issue.out_date,
            Issue.state_id.label('s_id'),
            State.s_name.label('state'),
            Issue.note,
            Issue.team_id.label('t_id'),
            Group_T.g_name.label('team'),
            Issue.group_id.label('g_id'),
            Group_G.g_name.label('group'),
            Issue.area_id.label('a_id'),
            Area.a_name.label('area'),
            Issue.fault_id.label('f_id'),
            Fault.f_name.label('fault'),
            Issue.ongoing_days,
            Issue.blocked_days,
            Issue.rcfound_days,
            Issue.knife,
            Issue.in_rft_day,
            Issue.rft_fcc_day,
            Issue.fcc_closed_day,
            Issue.u_id
        ]

        extended_table = Issue.query.outerjoin(Issue.category).outerjoin(Issue.release).\
            outerjoin(Issue.state).outerjoin(Group_T, Issue.team).outerjoin(Group_G, Issue.group).\
            outerjoin(Issue.area).outerjoin(Issue.fault).with_entities(*ret_col)

        issue_obj = extended_table.filter(db_filter).order_by(order_by).offset(offset).limit(limit).all()
        return issue_obj

    @staticmethod
    def insert(issue_dict):
        issue_obj = Issue(**issue_dict)
        db.session.add(issue_obj)
        db.session.commit()

    @staticmethod
    def delete(i_id):
        issue_obj = Issue.query.get(i_id)
        db.session.delete(issue_obj)
        db.session.commit()

    @staticmethod
    def update(i_id, issue_dict):
        Issue.query.filter(Issue.i_id==i_id).update(issue_dict)
        db.session.commit()
