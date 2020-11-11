from blog import models, db
from blog.models import Entry

def load():
    posts_list = []

    for entry in models.Entry.query.all():
        temp_post = {}
        temp_post["title"] = entry.title
        temp_post["body"] = entry.body
        temp_post["pub_date"] = entry.pub_date
        temp_post["is_published"] = entry.is_published
        temp_post["id"] = entry.id
        if temp_post["is_published"]:
            posts_list.append(temp_post)
 
    return posts_list

def load_drafts():
    drafts = Entry.query.filter_by(is_published=False)
    return drafts

def remove_post(id):
    post = Entry.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()