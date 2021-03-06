from . import ModelMixin
from . import db
from .blogCate import blogCategory


class blogTag(db.Model, ModelMixin):
    __tablename__ = 'blog_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    cate_id = db.Column(db.Integer, db.ForeignKey('blog_categories.id'))
    category = db.relationship('blogCategory', backref=db.backref('tags', lazy='dynamic'))

    def __init__(self, form):
        self.name = form.get('name', '')

    def add_cate(self, form):
        name = form.get('cate', '')
        c = blogCategory.query.filter_by(name=name).first()
        if c is not None:
            self.cate_id = c.id

    def update(self, form):
        self.name = form.get('name', self.name)
        self.add_cate(form)
