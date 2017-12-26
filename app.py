import base
from flask_security import Security, SQLAlchemyUserDatastore
import model.article
import flask_admin

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


admin = flask_admin.Admin(base.app, template_mode='bootstrap3')
admin.add_view(base.RoleModelView(base.Role, base.db.session))
admin.add_view(base.UserModelView(base.User, base.db.session))
admin.add_view(base.PermissionModelView(base.Permission, base.db.session))
admin.add_view(base.MyModelView(base.Router, base.db.session))
admin.add_view(model.article.ArticleView(
    model.article.Article, base.db.session))
admin.add_view(model.article.CategoryView(
    model.article.Category, base.db.session))


if __name__ == '__main__':
    base.app.jinja_env.auto_reload = True
    # Start app
    base.app.run(debug=True, port=5000)
