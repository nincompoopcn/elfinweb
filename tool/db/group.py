from .maintenance_db import db, BaseModel

class Group(BaseModel):
    __tablename__ = 'groups'
    g_id = db.Column(db.Integer, primary_key=True)
    g_name = db.Column(db.Unicode(64), nullable=False, unique=True)
    pr_name = db.Column(db.Unicode(64), unique=True)
    in_ps = db.Column(db.Boolean, nullable=False)
    member = db.Column(db.UnicodeText)
    description = db.Column(db.Unicode(100), default='')

    @staticmethod
    def insert_fake_group():
        groups = {'L2':False, 'MAC PS':False, 'UM':False, 'LOM':False,
                  'TRS':False, 'MW':False, 'HW':False, 'SPEC':False,
                  'MCUHWAPI':True, 'UPHWAPI':True, 'LCPLFS':True,
                  'LSPLFS':True, 'CCSMCU':True, '3G DL':False,
                   '3G UL':False, 'DLPHY':False, 'ULPHY':False}
        for c in groups:
            cat = Group.query.filter_by(g_name=c).first()
            if cat is None:
                cat = Group(g_name=c, in_ps=groups[c])
                db.session.add(cat)
        db.session.commit()

    def __repr__(self):
        return '<Group %r>' % self.g_name

    @staticmethod
    def select(db_filter=True, order_by=None):
        ret_col =  [
            Group.g_id.label('t_id'),
            Group.g_id.label('g_id'),
            Group.g_name.label('t_name'),
            Group.g_name.label('g_name'),
            Group.pr_name,
            Group.member,
            Group.description
        ]

        res = Group.query.with_entities(*ret_col).filter(db_filter).order_by(order_by).all()
        return res
        
    @staticmethod
    def update(g_id, group_dict):
        Group.query.filter(Group.g_id==g_id).update(group_dict)
        db.session.commit()