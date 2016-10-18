from . import ModelMixin
from . import db


class blogCategory(db.Model, ModelMixin):
    __tablename__ = 'blog_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))

    def __init__(self, form):
        self.name = form.get('name', '')
        self.description = form.get('description', '')
