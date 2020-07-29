
from flask import render_template, url_for, flash, redirect, request, jsonify
from mindful import db, app
from flask_login import current_user
from mindful.forms import CheckIn
from mindful.models import User, Mood

@app.route("/")
@app.route("/home")
def home():
    posts = Mood.query.all()
    return render_template('home.html', posts=posts)

@app.route("/dev")
def dev():
    return render_template('credits.html')

@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


@app.route("/termsofuse")
def termsofuse():
    return render_template('termsofuse.html')


@app.route("/checkin/new", methods=['GET', 'POST'])
def checkin():
    form = CheckIn()
    if form.validate_on_submit():
        if form.mood0.data == True:
            post = Mood(rating=0, user_id=1, content=content)
            pass
        if(form.mood1.data == True):
            post = Mood(rating=1, user_id=1)
            pass
        if(form.mood2.data == True):
            post = Mood(rating=2, user_id=1)
            pass
        else:
            pass
        if post:
            db.session.add(post)
            db.session.commit()
            flash('Thanks for your feedback', 'success')
        else:
            flash('failed to save response')
        return redirect(url_for('home'))
    return render_template('checkin.html', title='Mood',
                           form=form, legend='How are you feeling today?')


@app.route("/users/<user>/checkin", methods=['POST'])
def checkin_post(user_id):
    content = request.json

    #TODO: Sanitize input
    if (0 < content.rating and content.rating < 4):
        post = Mood(rating = content.rating, user_id = content.user_id)
    if post:
        db.session.add(post)
        db.session.commit()
        flash('Thanks for your feedback', 'success')
    else:
        flash('failed to save response')
    return content

@app.route("/resources")
def resources():
    return render_template("resources.html")