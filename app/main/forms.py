from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class BlogForm(FlaskForm):
    title=StringField('Blog Title')
    category=SelectField(u'Blog Category',
                         choices=['blogs'])
    blog=TextAreaField('Blog')
    submit=SubmitField('Submit')


class CommentForm(FlaskForm):
    comment=TextAreaField('Leave a Comment')
    submit=SubmitField(' Comment')


class UpdateBlogForm(FlaskForm):
    blog_title=StringField("Title", validators=[DataRequired()])
    blog_content=TextAreaField("Type Updates", validators=[DataRequired()])
    submit=SubmitField("Update")


class UpdateProfile(FlaskForm):
    bio=TextAreaField('Tell us about you.', validators=[DataRequired()])
    submit=SubmitField('Submit')
