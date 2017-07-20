# !/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from .. import db
from ..models import User
from .form import LoginForm, RegistrationForm, ChangePasswordForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
# 关闭注册功能
#        db.session.commit()
        flash('You can login now')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/ChangePassword', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            if current_user.password != fom.old_password.data:
                current_user.password = form.password.data
                db.session.add(current_user)
                flash('Password has been updated')
                return redirect(url_for('main.index'))
            else:
                flash('You just remember your password :)')
        else:
            flash('Invalid password')
    return render_template('auth/change_ps&email.html', form=form)
