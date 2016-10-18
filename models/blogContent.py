from . import ModelMixin
from . import db, blog_tags
from . import datetime
from .blogTag import blogTag
from .blogCate import blogCategory
from utils import log


class blogContent(db.Model, ModelMixin):
    __tablename__ = 'blog_contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    draft = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # relationship with category
    cate_id = db.Column(db.Integer, db.ForeignKey('blog_categories.id'))
    tags = db.relationship('blogTag', secondary=blog_tags, passive_deletes=True,
                           backref=db.backref('content', lazy="dynamic"))
    category = db.relationship('blogCategory',backref=db.backref('content', lazy='dynamic'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')

    def gen_tags(self, form):
        data = form.get('tag', '')
        log('data', data)
        tag_list = data.split(',')
        for tag in tag_list:
            t = blogTag.query.filter_by(name=tag).first()
            if t is not None:
                self.tags.append(t)
                log('self.tags', self.tags)

    def remove_tags(self, form):
        data = form.get('tag', '')
        tag_list = data.split(',')
        for tag in tag_list:
            t = blogTag.query.filter_by(name=tag).first()
            if t is not None:
                self.tags.remove(t)

    def add_cate(self, form):
        name = form.get('cate', '')
        c = blogCategory.query.filter_by(name=name).first()
        if c is not None:
            self.cate_id = c.id

    def get_create_time(self):
        return self.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def update(self, form):
        self.title = form.get('title', self.title)
        self.content = form.get('content', self.content)
        self.add_cate(form)
        self.gen_tags(form)
