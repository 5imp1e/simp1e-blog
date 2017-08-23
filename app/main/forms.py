# !/usr/bin/env python
# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=([Required(), Length(1, 64)]))
    content = PageDownField('Write Now', validators=[Required()])
    summary = TextAreaField('Summary', validators=[Required()])
    submit = SubmitField('Submit')
