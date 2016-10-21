from routes import *
from utils import admin_required, log, login_required, current_user
from models.bbsContent import bbsContent
from models.bbsNode import bbsNode
from models.bbsComment import bbsComment
from models.bbsTag import bbsTag


main = Blueprint("bbs_content", __name__)


@main.route('/node/<int:id>')
def node_content(id):
    u = current_user()
    n = bbsNode.query.get(id)
    c = bbsContent.query.filter_by(node_id=id).all()
    return render_template('bbs/content_list.html', contents=c, u=u, node=n)


@main.route('/')
def content_show():
    u = current_user()
    c = bbsContent.query.all()
    return render_template('bbs/content_show.html', contents=c, u=u)


@main.route('/<int:id>')
def content_get(id):
    u = current_user()
    c = bbsContent.query.get(id)
    return render_template('bbs/content_get.html', content=c, u=u)


@main.route('/edit/all')
@login_required
def content_edit_all():
    u = current_user()
    c = bbsContent.query.all()
    return render_template('bbs/content_edit_all.html', contents=c, u=u)


@main.route('/edit/<int:id>')
@login_required
def content_edit(id):
    u = current_user()
    c = bbsContent.query.get(id)
    return render_template('bbs/content_edit.html', content=c, u=u)


@main.route('/add', methods=['POST'])
@login_required
def content_add():
    form = request.form
    c = bbsContent(form)
    c.add_node(form)
    c.gen_tags(form)
    c.draft = False
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/delete/<int:id>')
@login_required
def content_delete(id):
    c = bbsContent.query.get(id)
    c.delete()
    return redirect(url_for('.content_show'))


@main.route('/update/<int:id>', methods=['POST'])
@login_required
def content_update(id):
    form = request.form
    c = bbsContent.query.get(id)
    c.update(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/update/node/<int:id>', methods=['POST'])
@login_required
def node_update(id):
    form = request.form
    c = bbsContent.query.get(id)
    c.add_node(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/update/tag/<int:id>', methods=['POST'])
@login_required
def tag_update(id):
    form = request.form
    c = bbsContent.query.get(id)
    c.gen_tags(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/remove/<int:id>', methods=['POST'])
@login_required
def tag_remove(id):
    form = request.form
    c = bbsContent.query.get(id)
    c.remove_tags(form)
    c.save()
    return redirect(url_for('.content_show'))


@main.route('/draft')
@login_required
def draft_show():
    u = current_user()
    t = bbsTag.query.all()
    n = bbsNode.query.all()
    return render_template('bbs/draft.html', nodes=n, tags=t, u=u)


@main.route('/draft/add', methods=['POST'])
@login_required
def draft_add():
    u = current_user()
    form = request.form
    c = bbsContent(form)
    c.add_node(form)
    c.gen_tags(form)
    c.user_id = u.id
    c.save()
    return redirect(url_for('.node_content', id=c.node_id))


@main.route('/comment/add', methods=['POST'])
@login_required
def add_comment():
    u = current_user()
    form = request.form
    c = bbsComment(form)
    c.author_id = u.id
    c.content_id = form.get('content_id', -1)
    c.save()
    return redirect(url_for('.content_get', id=c.content_id))
