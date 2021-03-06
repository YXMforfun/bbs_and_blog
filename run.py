from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import pymysql

from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.user import User
from models.bbsNode import bbsNode
from models.bbsContent import bbsContent
from models.bbsComment import bbsComment
from models.bbsTag import bbsTag
from models.weibo import Weibo
from models.weiboComment import WeiboComment
from models.blogContent import blogContent
from models.blogCate import blogCategory
from models.blogTag import blogTag


app = Flask(__name__)
#db_path = 'app.sqlite'
manager = Manager(app)


def register_routes(app):
    from routes.home import main as routes_home
    from routes.bbsNode import main as routes_bbs_node
    from routes.bbsContent import main as routes_bbs_content
    from routes.bbsTag import main as routes_bbs_tag
    from routes.user import main as routes_user
    from routes.weibo import main as routes_weibo
    from routes.blogCate import main as routes_blog_cate
    from routes.blogContent import main as routes_blog_content
    from routes.blogTag import main as routes_blog_tag
    from api.user import main as routes_api_user
    from api.weibo import main as routes_api_weibo

    app.register_blueprint(routes_home)
    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_bbs_tag, url_prefix='/bbs/tag')
    app.register_blueprint(routes_bbs_node, url_prefix='/bbs/node')
    app.register_blueprint(routes_bbs_content, url_prefix='/bbs/content')
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_blog_cate, url_prefix='/blog/cate')
    app.register_blueprint(routes_blog_content, url_prefix='/blog/content')
    app.register_blueprint(routes_blog_tag, url_prefix='/blog/tag')
    app.register_blueprint(routes_api_user, url_prefix='/api/user')
    app.register_blueprint(routes_api_weibo, url_prefix='/api/weibo')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/bbs'
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    print('server run')
    # app = configured_app()
    config = dict(
        debug=False,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)

@manager.command
def create_all():
    db.drop_all()
    db.create_all()

def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()

# gunicorn -b '0.0.0.0:80' redischat:app
