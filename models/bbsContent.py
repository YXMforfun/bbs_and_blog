from . import ModelMixin
from . import db, bbs_tags
from . import datetime
from .bbsTag import bbsTag
from .bbsNode import bbsNode
from .bbsComment import bbsComment
from utils import log


class bbsContent(db.Model, ModelMixin):
    __tablename__ = 'bbs_contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('bbs_nodes.id'))
    tags = db.relationship('bbsTag', secondary=bbs_tags, passive_deletes=True,
                           backref=db.backref('content', lazy='dynamic'))
    node = db.relationship('bbsNode',backref=db.backref('content', lazy='dynamic'))
    comment = db.relationship('bbsComment', backref='content', lazy='dynamic')

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')

    def gen_tags(self, form):
        tag1 = form.get('tag1', '')
        tag2 = form.get('tag2', '')
        tag_list = [tag1] + [tag2]
        for tag in tag_list:
            t = bbsTag.query.filter_by(name=tag).first()
            log('t', t)
            if t is not None:
                self.tags.append(t)
                log(self.tags, 'self.tags')

    def remove_tags(self, form):
        data = form.get('tag', '')
        tag_list = data.split(',')
        for tag in tag_list:
            t = bbsTag.query.filter_by(name=tag).first()
            if t is not None:
                self.tags.remove(t)

    def add_node(self, form):
        name = form.get('node', '')
        n = bbsNode.query.filter_by(name=name).first()
        if n is not None:
            self.node_id = n.id

    def get_create_time(self):
        return self.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def update(self, form):
        self.title = form.get('title', self.title)
        self.content = form.get('content', self.content)
        self.add_node(form)
        self.gen_tags(form)
