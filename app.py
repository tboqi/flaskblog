import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_babelex import Babel

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'


class Role(db.Model, RoleMixin):
    __tablename__ = 'auth_roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    # users = db.relationship("User",
    #                         backref=db.backref('auth_users'))

    def __str__(self):
        return self.name


class Permission(db.Model, RoleMixin):
    __tablename__ = 'auth_permissions'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

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
        return self.email


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
    column_labels = {'name': '名称'}


class UserModelView(MyModelView):
    form_excluded_columns = ['created_at']
    column_exclude_list = ['password', ]

    column_labels = {'role': '角色', 'name': '用户名', 'password': '密码',
                     'active': '激活', 'created_at': '创建时间'}


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
def welcome():
    if not current_user.is_active or not current_user.is_authenticated:
        return redirect(url_for('security.login', next=request.url))

    return render_template('admin/welcome.html')

# Create admin
admin = flask_admin.Admin(app, template_mode='bootstrap3')

# Add model views
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(PermissionModelView(Permission, db.session))

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
