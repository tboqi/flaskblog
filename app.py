import base
import flask_admin
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from model.article import Article, Category, ArticleView, CategoryView


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(base.db, base.User, base.Role)
security = Security(base.app, user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


class MyHomeView(flask_admin.AdminIndexView):

    @flask_admin.expose('/')
    def index(self):
        if not current_user.is_active or not current_user.is_authenticated or not current_user.role:
            return redirect(url_for('security.login', next=request.url))

        return self.render('admin/index.html')

    @flask_admin.expose('/welcome/')
    def welcome(self):
        return '欢迎'

admin = flask_admin.Admin(
    base.app, template_mode='bootstrap3', index_view=MyHomeView())
admin.add_view(base.RoleModelView(base.Role, base.db.session))
admin.add_view(base.UserModelView(base.User, base.db.session))
admin.add_view(base.PermissionModelView(base.Permission, base.db.session))
admin.add_view(base.MyModelView(base.Router, base.db.session))
admin.add_view(ArticleView(Article, base.db.session))
admin.add_view(CategoryView(Category, base.db.session))


@base.app.route('/')
def index():
    page = int(request.args.get('page', 1))
    per_page = 10
    paginate = Article.query.order_by(Article.id.desc())
    paginate = paginate.paginate(page, per_page, False)
    object_list = paginate.items
    return render_template('index.html',
                           categories=Category.query.all(),
                           articles=object_list, paginate=paginate)


@base.app.route('/article/listbycate')
def articlesByCate():
    page = int(request.args.get('page', 1))
    per_page = 10
    paginate = Article.query
    paginate = paginate.filter(Article.category_id == request.args.get('id'))
    paginate = paginate.order_by(Article.id.desc())
    paginate = paginate.paginate(page, per_page, False)
    object_list = paginate.items
    return render_template('index.html',
                           categories=Category.query.all(),
                           articles=object_list, paginate=paginate, cate_id=int(request.args.get('id')))


@base.app.route('/article/view')
def articleView():
    return render_template('article_view.html',
                           categories=Category.query.all(),
                           article=Article.query.filter(Article.id == request.args.get('id')).one())

if __name__ == '__main__':
    base.app.jinja_env.auto_reload = True
    base.app.run(debug=True, port=5000)
