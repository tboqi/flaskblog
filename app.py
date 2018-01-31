import base
import flask_admin
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from model.article import Article, Category, ArticleView, CategoryView
from flask_admin.base import MenuLink, Admin, BaseView, expose

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
    base.app,
    '后台管理',
    base_template='my_master.html',
    template_mode='bootstrap3',
)
admin.add_view(ArticleView(Article, base.db.session,
                           name='文章管理', category='文章管理'))
admin.add_view(CategoryView(Category, base.db.session,
                            name='分类管理', category='文章管理'))
admin.add_view(base.RoleModelView(
    base.Role, base.db.session, name='角色管理', category='系统管理'))
admin.add_view(base.UserModelView(
    base.User, base.db.session, name='用户管理', category='系统管理'))
admin.add_view(base.PermissionModelView(base.Permission,
                                        base.db.session, name='权限管理', category='系统管理'))
admin.add_view(base.MyModelView(
    base.Router, base.db.session, name='路由管理', category='系统管理'))
admin.add_link(MenuLink(name='博客首页', url='/'))

title = '一只小虫吞太阳'
seo = {'title': title, 'description': '各种杂谈及技术的记录, 记录生活与学习',
       'keywords': 'php,python'}


@base.app.route('/')
def index():
    page = int(request.args.get('page', 1))
    per_page = 10
    paginate = Article.query.order_by(Article.id.desc())
    paginate = paginate.paginate(page, per_page, False)
    object_list = paginate.items

    return render_template('index.html',
                           categories=Category.query.all(), seo=seo, pageTitle='首页',
                           newArticles=Article.query.order_by(
                               Article.created_at.desc()).limit(10),
                           hotArticles=Article.query.order_by(
                               Article.view_num.desc()).limit(10),
                           articles=object_list, paginate=paginate)


@base.app.route('/article/listbycate/<cateid>')
def articlesByCate(cateid):
    page = int(request.args.get('page', 1))
    per_page = 10
    paginate = Article.query
    paginate = paginate.filter(Article.category_id == cateid)
    paginate = paginate.order_by(Article.id.desc())
    paginate = paginate.paginate(page, per_page, False)
    object_list = paginate.items
    category = Category.query.get(int(cateid))
    pageTitle = '分类:' + category.name + '的所有文章'
    seo = {'title': title, 'description': pageTitle,
           'keywords': category.name}
    return render_template('index.html',
                           categories=Category.query.all(), pageTitle='分类:' + category.name + '的所有文章', seo=seo,
                           newArticles=Article.query.order_by(
                               Article.created_at.desc()).limit(10),
                           hotArticles=Article.query.order_by(
                               Article.view_num.desc()).limit(10),
                           articles=object_list, paginate=paginate, cate_id=int(cateid))


@base.app.route('/article/listbytag/<tag>')
def articlesByTag(tag):
    page = int(request.args.get('page', 1))
    per_page = 10
    paginate = Article.query
    paginate = paginate.filter(
        Article.tags.like('%' + ',' + tag + ',' + '%'))
    paginate = paginate.order_by(Article.id.desc())
    paginate = paginate.paginate(page, per_page, False)
    object_list = paginate.items
    pageTitle = '标签:' + tag + '的所有文章'
    seo = {'title': title, 'description': pageTitle,
           'keywords': tag}
    return render_template('index.html',
                           categories=Category.query.all(), pageTitle=pageTitle, seo=seo,
                           newArticles=Article.query.order_by(
                               Article.created_at.desc()).limit(10),
                           hotArticles=Article.query.order_by(
                               Article.view_num.desc()).limit(10),
                           articles=object_list, paginate=paginate)


@base.app.route('/article/view/<id>')
def articleView(id):
    prevArt = Article.query.filter(
        Article.id > id).order_by(Article.id.asc()).first()
    nextArt = Article.query.filter(
        Article.id < id).order_by(Article.id.desc()).first()
    article = Article.query.get(id)
    article.view_num = article.view_num + 1
    base.db.session.add(article)
    base.db.session.commit()
    seo = {'title': title, 'description': article.summary,
           'keywords': article.tags.strip(',')}
    return render_template('article_view.html',
                           categories=Category.query.all(), pageTitle=article.title + ' - ' + article.category.name, seo=seo,
                           article=article,
                           newArticles=Article.query.order_by(
                               Article.created_at.desc()).limit(10),
                           hotArticles=Article.query.order_by(
                               Article.view_num.desc()).limit(10),
                           prevArt=prevArt, nextArt=nextArt)

if __name__ == '__main__':
    base.app.jinja_env.auto_reload = True
    base.app.run(debug=True, port=5000)
