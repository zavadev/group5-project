from flask import Blueprint, render_template, request
from app.models.db import db
from app.models.tag import Tag
from app.forms.create_tag_form import CreateTagForm
from app.api.auth_routes import validation_errors_to_error_messages

tags_router = Blueprint("tags", __name__)

# GET all Tags
@tags_router.route("/all")
def all_tags():
  results = Tag.query.all()
  print(results)
  return { "tags": [tag.to_dict() for tag in results] }

# POST (CREATE) new Tag
@tags_router.route("/create_tag", methods=["GET", "POST"])
def create_tag():
  form = CreateTagForm()
  form['csrf_token'].data = request.cookies['csrf_token']

  if form.validate_on_submit():
    new_tag = Tag(
      tag_name = form.data['tag_name']
    )
    db.session.add(new_tag)
    db.session.commit()
    return new_tag.to_dict()

  return {"errors": validation_errors_to_error_messages(form.errors)}
