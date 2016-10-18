from . import ModelMixin
from . import db
from .bbsNode import bbsNode


class bbsTag(db.Model, ModelMixin):
    __tablename__ = 'bbs_tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    node_id = db.Column(db.Integer, db.ForeignKey('bbs_nodes.id'))
    node = db.relationship('bbsNode', backref=db.backref('tags', lazy='dynamic'))

    def __init__(self, form):
        self.name = form.get('name', '')

    def add_node(self, form):
        name = form.get('node', '')
        n = bbsNode.query.filter_by(name=name).first()
        if n is not None:
            self.node_id = n.id

    def update(self, form):
        self.name = form.get('name', self.name)
        self.add_node(form)
