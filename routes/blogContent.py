from routes import *
from utils import admin_required, log, login_required, current_user
from models.blogContent import blogContent

main = Blueprint("blog_content", __name__)


@main.route('/cate/<int:id>')
def cate_content(id):
    c = blogContent.query.filter_by(cate_id=id, draft=False).all()
    return render_template('blog/content_show.html', contents=c)


@main.route('/')
def content_show():
    c = blogContent.query.filter_by(draft=False).all()
    return render_template('blog/content_show.html', contents=c)


@main.route('/edit/all')
@login_required
@admin_required
def content_edit_all():
    c = blogContent.query.all()
    return render_template('blog/content_edit_all.html', contents=c)


@main.route('/edit/<int:id>')
@login_required
@admin_required
def content_edit(id):
    c = blogContent.query.get(id)
    return render_template('blog/content_edit.html', content=c)


@main.route('/add', methods=['POST'])
@login_required
@admin_required
def content_add():
    form = request.form
    c = blogContent(form)
    c.add_cate(form)
    c.gen_tags(form)
    c.draft = False
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/delete/<int:id>')
@login_required
@admin_required
def content_delete(id):
    c = blogContent.query.get(id)
    c.delete()
    return redirect(url_for('.content_show'))


@main.route('/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def content_update(id):
    form = request.form
    c = blogContent.query.get(id)
    c.update(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/update/cate/<int:id>', methods=['POST'])
@login_required
@admin_required
def cate_update(id):
    form = request.form
    c = blogContent.query.get(id)
    c.add_cate(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/update/tag/<int:id>', methods=['POST'])
@login_required
@admin_required
def tag_update(id):
    form = request.form
    c = blogContent.query.get(id)
    c.gen_tags(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/remove/<int:id>', methods=['POST'])
@login_required
@admin_required
def tag_remove(id):
    form = request.form
    c = blogContent.query.get(id)
    c.remove_tags(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/draft')
@login_required
@admin_required
def draft_show():
    c = blogContent.query.filter_by(draft=True).all()
    return render_template('blog/draft.html', contents=c)


@main.route('/draft/add', methods=['POST'])
@login_required
@admin_required
def draft_add():
    form = request.form
    c = blogContent(form)
    c.add_cate(form)
    c.gen_tags(form)
    log('c', c)
    c.save()
    return redirect(url_for('.draft_show'))


@main.route('/publish/<int:id>')
@login_required
@admin_required
def publish_content(id):
    c = blogContent.query.get(id)
    c.draft = False
    c.save()
    return redirect(url_for('.content_show'))


