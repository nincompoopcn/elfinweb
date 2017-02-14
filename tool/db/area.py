from .maintenance_db import db, BaseModel

from .group import Group

class Area(BaseModel):
    __tablename__ = 'areas'
    a_id = db.Column(db.Integer, primary_key=True)
    a_name = db.Column(db.Unicode(64), nullable=False, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.g_id'), nullable=False)
    description = db.Column(db.Unicode(100), default='')

    group = db.relationship('Group', foreign_keys=group_id)

    @staticmethod
    def insert_fake_area():
        areas = {'CCSRT':'UPHWAPI', 'EM':'UPHWAPI', 'DSPHWAPI':'UPHWAPI',
                 'Clock & Sync':'MCUHWAPI', 'BBB':'MCUHWAPI', 'Operability':'MCUHWAPI',
                 'Startup and Loading':'LCPLFS', 'Kernal':'LCPLFS', 'Board Interface':'LCPLFS',
                 'High Speed':'LSPLFS'}
        for c in areas:
            cat = Area.query.filter_by(a_name=c).first()
            if cat is None:
                cat = Area(a_name=c, group=Group.query.filter_by(g_name=areas[c]).first())
            db.session.add(cat)
        db.session.commit()

    def __repr__(self):
        return '<Area %r>' % self.a_name

    @staticmethod
    def select(db_filter=True, order_by=None):
        ret_col =  [
            Area.a_id,
            Area.a_name,
            Area.group_id.label('g_id'),
            Group.g_name.label('group'),
            Area.description
        ]

        extended_table = Area.query.outerjoin(Area.group).with_entities(*ret_col)

        res = extended_table.filter(db_filter).order_by(order_by).all()
        return res