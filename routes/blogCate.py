from routes import *
from utils import admin_required, login_required
from models.blogTag import blogTag
from models.blogCate import blogCategory
from models.blogContent import blogContent


main = Blueprint("blog_cate", __name__)


@main.route('/')
def cate_show():
    c = blogCategory.query.all()
    return render_template('blog/cate_show.html', cates=c)


@main.route('/<int:id>')
def cate_get(id):
    c = blogCategory.query.get(id)
    return render_template('blog/cate_show.html', cates=c)


@main.route('/add', methods=['POST'])
@login_required
@admin_required
def cate_add():
    form = request.form
    c = blogCategory(form)
    c.save()
    return redirect(url_for('.cate_show'))


@main.route('/delete/<int:id>')
@login_required
@admin_required
def cate_delete(id):
    c = blogCategory.query.get(id)
    c.delete()
    return redirect(url_for('.cate_show'))


@main.route('/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def cate_update(id):
    form = request.form
    c = blogCategory.query.get(id)
    c.name = form.get('name', '')
    c.description = form.get('description', '')
    c.save()
    return redirect(url_for('.cate_show'))

