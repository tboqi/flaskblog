from base import db, MyModelView, CKTextAreaField, User
import datetime
from flask_security import current_user


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
    category = db.relationship('Category',
                               backref=db.backref('article_categories'))
    category_id = db.Column(db.Integer, db.ForeignKey('article_categories.id'))
    tags = db.Column(db.String(80))

    def __str__(self):
        return self.title


class Category(db.Model):
    __tablename__ = 'article_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    def __str__(self):
        return self.name


class ArticleView(MyModelView):
    form_excluded_columns = ['created_at', 'updated_at', 'author', 'author_id']
    column_exclude_list = ['content', ]

    column_labels = {'author': '作者', 'title': '标题', 'content': '内容',
                     'created_at': '创建时间', 'updated_at': '更新时间'}

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'content': CKTextAreaField
    }
    column_formatters = dict(tags=lambda v, c, m, p: m.tags.strip(','))

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = datetime.datetime.today()
            model.author_id = current_user.id
            pass

        model.updated_at = datetime.datetime.today()
        model.tags.strip(',')
        model.tags = ',' + model.tags + ','


class CategoryView(MyModelView):
    form_excluded_columns = ['articles']
    column_labels = {'name': '分类名'}
