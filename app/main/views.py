# !/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import render_template, session, redirect, url_for, current_app, request, flash
from flask_login import current_user, login_required
from .. import db
from ..models import User, Post
from . import main
from .forms import PostForm


#@main.route('/')
# def index():
#    return render_template('index.html')


@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()[:9]
    return render_template('index.html', posts=posts)


@main.route('/post_list/', methods=['GET', 'POST'])
def post_list():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('post_list.html', posts=posts, pagination=pagination)


@main.route('/post_detail/<string:title>', methods=['GET', 'POST'])
def post_detail(title):
    #    title = title.replace(' ', '_')
    post = Post.query.filter_by(title=title).first_or_404()
    return render_template('post_detail.html', post=post)


@main.route('/post_blog/', methods=['GET', 'POST'])
@login_required
def post_blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data,
                    author=current_user._get_current_object(),
                    title=form.title.data,
                    summary=form.summary.data)
        db.session.add(post)
#        db.session.commit()
        return redirect(url_for('main.post_detail'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('post_blog.html', form=form, posts=posts)


@main.route('/edit/<string:title>', methods=['GET', 'POST'])
@login_required
def edit(title):
    post = Post.query.filter_by(title=title).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        post.summary = form.summary.data
        post.title = form.title.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated')
        return redirect(url_for('post_detial', title=title))
    form.title.data = post.title
    form.summary.data = post.summary
    form.content.data = post.content
    return render_template('edit.html', form=form)


@main.route('/delete/<string:title>', methods=['GET', 'POST'])
@login_required
def delete(title):
    post = Post.query.filter_by(title=title).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        try:
            db.session.delete(title)
        except:
            db.session.rollback()
            flash('delete error')
        else:
            flash('success!')
    return render_template('post_list.html')
