from routes import *
from utils import admin_required, login_required
from models.blogTag import blogTag



main = Blueprint("blog_tag", __name__)


@main.route('/')
def tag_show():
    t = blogTag.query.all()
    return render_template('blog/tag_show.html', tags=t)


@main.route('/<int:id>')
def tag_get(id):
    t = blogTag.query.get(id)
    return render_template('blog/tag_show.html', tags=t)


@main.route('/add', methods=['POST'])
@login_required
@admin_required
def tag_add():
    form = request.form
    t = blogTag(form)
    t.add_cate(form)
    t.save()
    return redirect(url_for('.tag_show'))


@main.route('/delete/<int:id>')
@login_required
@admin_required
def tag_delete(id):
    t = blogTag.query.get(id)
    t.delete()
    return redirect(url_for('.tag_show'))


@main.route('/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def tag_update(id):
    form = request.form
    t = blogTag.query.get(id)
    t.update(form)
    t.save()
    return redirect(url_for('.tag_show'))