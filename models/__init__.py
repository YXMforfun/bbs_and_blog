from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import url_for

db = SQLAlchemy()


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        # self.deleted = True
        # self.save()


bbs_tags = db.Table('bbs_tags_contents',
                    db.Column('tag_id', db.Integer, db.ForeignKey('bbs_tag.id', ondelete='CASCADE', onupdate='CASCADE')),
                    db.Column('content_id', db.Integer, db.ForeignKey('bbs_contents.id', ondelete='CASCADE', onupdate='CASCADE')))

blog_tags = db.Table('blog_tags_contents',
                     db.Column('tag_id', db.Integer, db.ForeignKey('blog_tags.id', ondelete='CASCADE', onupdate='CASCADE')),
                     db.Column('content_id', db.Integer, db.ForeignKey('blog_contents.id', ondelete='CASCADE', onupdate='CASCADE')))


"""
脚本的例子

apt-get install python3 python3-dev ....
pip3 install flask flask-script flask-migrate ....

import os

os.system('pip3 install flask')



"""