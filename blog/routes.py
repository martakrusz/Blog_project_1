from flask import render_template, request, redirect, url_for, flash, session
from blog import app, db, services
from blog.models import Entry
from blog.forms import EntryForm, LoginForm
import functools

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

@app.route("/", methods=["GET", "POST"])
def index():
   posts_list = services.load()
   if request.method == "POST":
      if request.form["btn"] == "Add New Post":
         return redirect(url_for("create_entry"))
      
   return render_template("homepage.html", all_posts=posts_list)

@app.route("/add", methods=["GET","POST"])
@login_required
def create_entry():
   return create_edit_entry()

@app.route("/edit/<int:entry_id>", methods=["GET","POST"])
@login_required
def edit_entry(entry_id):
   return create_edit_entry(entry_id)


@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)



@app.route("/drafts/", methods=['GET', 'POST'])
@login_required
def list_drafts():
   posts_list = services.load_drafts()
   if request.method == "POST":
      if request.form["btn"] == "Back":
         return redirect(url_for('index'))

   return render_template("drafts.html", all_posts=posts_list)

@app.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def remove_post(post_id):
   services.remove_post(post_id)
   flash('Post usunięto', 'success')
   return redirect(url_for('list_drafts'))


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))


def create_edit_entry(entry_id = 0):
   errors = None
   if entry_id == 0:
      entry_form = EntryForm()
   else:
      entry = Entry.query.filter_by(id=entry_id).first_or_404()
      entry_form = EntryForm(obj=entry)

   if request.method == "POST":
      if request.form["btn"] == "Save":
         if entry_form.validate_on_submit():
            if entry_id == 0:
               entry = Entry(
                              title = entry_form.title.data,
                              body = entry_form.body.data,
                              is_published =entry_form.is_published.data
                              )
               db.session.add(entry)
            else:
               entry_form.populate_obj(entry)
         else:
            errors = entry_form.errors
            flash('Nie wpowadzono zmian', 'danger')

      if request.form["btn"] == "Cancel":
         return redirect(url_for("index"))

      db.session.commit()
      flash('Zmiany dodane pomyślnie', 'success')
      return redirect(url_for("index"))

   return render_template("entry_form.html", entry_form=entry_form, errors=errors)