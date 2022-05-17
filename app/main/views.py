from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from ..models import Blogs, User, Comments, Quote
from . import main
from .. import db, photos
from .forms import BlogForm, CommentForm, UpdateProfile
from ..requests import get_quote


@main.route('/', methods=["GET"])
def index(cate=None):
    '''
    index page

    '''
    quote=get_quote()
    blogs=Blogs.get_blogs(cate)
    title='SASSY BLOG POST'
    return render_template('index.html', quote=quote, title=title, blogs=blogs)


@main.route('/blog/', methods=['GET', 'POST'])
@login_required
def new_blog():
    form=BlogForm()

    if form.validate_on_submit():
        category=form.category.data
        blog=form.blog.data
        title=form.title.data

        new_blog=Blogs(title=title, category=category, blog=blog, user_id=current_user.id)

        title='New Blog'

        new_blog.save_blogs()

        return redirect(url_for('main.index'))

    return render_template('blog.html', blog_entry=form)


@main.route('/categories/<cate>', methods=["GET"])
def category(cate):
    """
    function to return the pitches by category
    """
    category=Blogs.get_blogs(cate)

    title=f'{cate}'
    return render_template('categories.html', title=title, category=category)


@main.route('/user/<uname>', methods=["GET"])
def profile(uname):
    user=User.query.filter_by(author=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user=User.query.filter_by(author=uname).first()
    if user is None:
        abort(404)

    form=UpdateProfile()

    if form.validate_on_submit():
        user.bio=form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.author))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user=User.query.filter_by(author=uname).first()
    if 'photo' in request.files:
        filename=photos.save(request.files['photo'])
        path=f'photos/{filename}'
        user.profile_pic_path=path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/comments/<id>', methods=["GET"])
@login_required
def comment(comment_id):
    '''
    function to return the comments
    '''
    com=Comments.get_comment(comment_id)
    # print(com)
    title='Blog Comments'
    return render_template('comments.html', comment=com, title=title)


@main.route('/new_comment/<int:blogs_id>', methods=['GET', 'POST'])
@login_required
def new_comment(blogs_id):
    blogs=Blogs.query.filter_by(id=blogs_id).first()
    form=CommentForm()

    if form.validate_on_submit():
        comment=form.comment.data

        new_comment=Comments(comment=comment, user_id=current_user.id, blogs_id=blogs_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New Blog'
    return render_template('new_comment.html', title=title, comment_form=form, blogs_id=blogs_id)


@main.route("/blog/<int:id>/delete", methods=["POST"])
@login_required
def delete_comment(id):
    comment=Comments.get_comment(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for(".new_comment", id=comment.id))


@main.route("/blog/<int:id>/delete")
@login_required
def delete_blog(id):
    blog=Blogs.get_blogs(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for(".index", id=blog.id))
