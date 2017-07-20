# !/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import render_template, session, redirect, url_for, current_app, request
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
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data,
                    author='Simp1e', title=form.title.data,
                    summary=form.summary.data)
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()[:9]
    return render_template('index.html', form=form, posts=posts)


@main.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data,
                    author='Simp1e', title=form.title.data,
                    summary=form.summary.data)
        db.session.add(post)
        return redirect(url_for('.post'))
#    posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('post.html', form=form, posts=posts, pagination=pagination)


@main.route('/post_blog', methods=['GET', 'POST'])
@login_required
def post_blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data,
                    author='Simp1e', title=form.title.data,
                    summary=form.summary.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post'))
    return render_template('post.html', form=form)
