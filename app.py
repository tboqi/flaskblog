import os
import datetime
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_babelex import Babel
from wtforms import TextAreaField
from wtforms.widgets import TextArea


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'


role_permission_ln = db.Table(
    'auth_role_permission_ln',
    db.Column('permission_id', db.Integer(),
              db.ForeignKey('auth_permissions.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('auth_roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'auth_roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.relationship('Permission', secondary=role_permission_ln,
                                  backref=db.backref('auth_roles', lazy='dynamic'))

    def __str__(self):
        return self.name


class Permission(db.Model, RoleMixin):
    __tablename__ = 'auth_permissions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    # routers = db.relationship("Router",
    #                           backref=db.backref('auth_routers'))

    def __str__(self):
        return self.name


class Router(db.Model):
    __tablename__ = 'auth_routers'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    router = db.Column(db.String(255))
    name = db.Column(db.String(255))
    permission = db.relationship('Permission',
                                 backref=db.backref('auth_permissions'))
    permission_id = db.Column(db.Integer, db.ForeignKey('auth_permissions.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('auth_routers.id'))
    parent = db.relationship('Router',
                             backref=db.backref('auth_routers'), remote_side=[id])

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    role = db.relationship('Role',
                           backref=db.backref('auth_roles'))
    role_id = db.Column(db.Integer, db.ForeignKey('auth_roles.id'))

    def __str__(self):
        return self.name


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    author = db.relationship('User',
                             backref=db.backref('auth_users'))
    author_id = db.Column(db.Integer, db.ForeignKey('auth_users.id'))

    def __str__(self):
        return self.name


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        # if current_user.has_role('superuser'):
        #     return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        # if not self.is_accessible():
        #     if current_user.is_authenticated:
        #         # permission denied
        #         abort(403)
        #     else:
        #         # login
        #         return redirect(url_for('security.login', next=request.url))


class RoleModelView(MyModelView):
    column_labels = {'name': '角色名', 'description': '描述'}


class PermissionModelView(MyModelView):
    form_excluded_columns = ['routers']
    column_labels = {'name': '名称'}


class UserModelView(MyModelView):
    form_excluded_columns = ['created_at']
    column_exclude_list = ['password', ]

    column_labels = {'role': '角色', 'name': '用户名', 'password': '密码',
                     'active': '激活', 'created_at': '创建时间'}


class CKTextAreaWidget(TextArea):

    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ArticleModelView(MyModelView):
    form_excluded_columns = ['created_at', 'updated_at', 'author', 'author_id']
    column_exclude_list = ['content', ]

    column_labels = {'author': '作者', 'title': '标题', 'content': '内容',
                     'created_at': '创建时间', 'updated_at': '更新时间'}

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'content': CKTextAreaField
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = datetime.datetime.today()
            model.author_id = current_user.id
            pass
        model.updated_at = datetime.datetime.today()
        pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/')
def admin_index():
    # or not current_user.has_role('superuser')
    if not current_user.is_active or not current_user.is_authenticated:
        return redirect(url_for('security.login', next=request.url))

    return render_template('admin/index.html')


@app.route('/admin/welcome')
def admin_welcome():
    return request.path

# Create admin
admin = flask_admin.Admin(app, template_mode='bootstrap3')

# Add model views
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(PermissionModelView(Permission, db.session))
admin.add_view(MyModelView(Router, db.session))
admin.add_view(ArticleModelView(Article, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


if __name__ == '__main__':
    # Start app
    app.run(debug=True, port=5000)
