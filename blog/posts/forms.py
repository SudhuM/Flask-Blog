from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired


class PostCreationForm(FlaskForm):

    title = StringField('Title', validators=[
        InputRequired(), DataRequired()])

    content = TextAreaField('Content', validators=[
        InputRequired(), DataRequired()])

    post = SubmitField('Post')


class EditPostForm(FlaskForm):

    title = StringField('Title', validators=[
        InputRequired(), DataRequired()])

    content = TextAreaField('Content', validators=[
        InputRequired(), DataRequired()])

    update = SubmitField('Update Post')
