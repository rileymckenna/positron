
from flask import render_template, url_for, flash, redirect, request, jsonify
from mindful import db, app
from flask_login import current_user
from mindful.forms import CheckIn
from mindful.models import User, Mood
import json


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
            post = Mood(rating=0, user_id=1)
            pass
        if(form.mood1.data == True):
            post = Mood(rating=1, user_id=1)
            pass
        if(form.mood2.data == True):
            post = Mood(rating=2, user_id=1)
            pass
        else:
            pass
        if(form.text.data != None):
            post.content = form.text.data
        if post:
            db.session.add(post)
            db.session.commit()
            flash('Thanks for your feedback', 'success')
        else:
            flash('failed to save response')
        return redirect(url_for('home'))
    return render_template('checkin.html', title='Mood',
                           form=form, legend='How are you feeling today?')


@app.route("/users/<user>", methods=['GET'])
def get_user(user):
    users = User.query.filter_by(teams_id=user).first()
    if(users == None):
        return "User not found"
    else:
        return render_template('user.html', user=users)


@app.route("/users/new", methods=['POST'])
def create_user():
    content = request.json
    tms_id = content['teams_id']

    if(tms_id != None):
        possible_user = User.query.filter_by(teams_id=tms_id).first()
        if(possible_user == None):
            user = User()
            user.teams_id = tms_id
            db.session.add(user)
            db.session.commit()
            urlRedirect = 'users/' + user.teams_id
            return redirect(url_for(urlRedirect), 200)
        else:
            return redirect(url_for('home'), 404)
    else:
        return redirect(url_for('home'), 404)


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/users/<user>/new", methods=['POST'])
def createUser(user):
    content = request.json

    # TODO: Sanitize input
    if (0 < content['rating'] and content['rating'] < 4):
        post = Mood(rating=content['rating'],
                    user_id=user, content=content['content'])
    if post:
        db.session.add(post)
        db.session.commit()
        flash('Thanks for your feedback', 'success')
    else:
        flash('failed to save response')
    return content
