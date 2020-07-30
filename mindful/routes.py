
from flask import render_template, url_for, flash, redirect, request, jsonify, Response
from mindful import db, app
from flask_login import current_user
from mindful.forms import CheckIn
from mindful.models import User, Mood
import json
from datetime import timedelta, date
import random


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', user="Company")

@app.route("/view")
def view():
    moods = Mood.query.all()
    return render_template('view.html', moods=moods)


@app.route("/data")
def data():
    moods = Mood.query.all()
    return jsonify([i.serialize for i in moods])

@app.route("/data/<user>")
def data_user(user):
    moods = Mood.query.filter_by(user_id=user)
    return jsonify([i.serialize for i in moods])


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
        if post:
            if(form.text != None):
                post.content = form.text.data
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
        jx = jsonify(users.serialize)
        return jx


@app.route("/users/<user>/details", methods=['GET'])
def get_user_details(user):
    users = Mood.query.filter_by(user_id=user).first()
    if(users == None):
        return "User details not found"
    else:
        return render_template('user.html', user=users)


@app.route("/users/new", methods=['POST'])
def create_user():
    content = request.json
    tms_id = content['teams_id']

    if(tms_id != None):
        possible_user = User.query.filter_by(teams_id=tms_id).first()
        if(possible_user == None):
            user = User(id=None, teams_id=tms_id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('get_user', user=user.teams_id), 200)
        else:
            return redirect(url_for('home'), 404)
    else:
        return redirect(url_for('home'), 404)


@app.route("/checkin", methods=['POST'])
def create_user_checkin():
    content = request.json
    rating = content['rating']
    text = content['content']
    idx = content['user_id']
    post = Mood(rating=rating, user_id=idx, content=text)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.full_serialize)


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/users/<user>/new", methods=['POST'])
def createUser(user):
    content = request.json

    # TODO: Sanitize input
    if (0 < content['rating'] and content['rating'] < 4):
        post = Mood(rating = content['rating'], user_id = user, content = content['content'])
    if post:
        db.session.add(post)
        db.session.commit()
        flash('Thanks for your feedback', 'success')
    else:
        flash('failed to save response')
    return content

@app.route("/users/<user>/moods", methods=['GET'])
def get_user_moods(user):
    users = User.query.filter_by(teams_id=user).first()
    if(users == None):
        return "User not found"
    else:
        return render_template('home.html', user=user)

@app.route("/populate/<emotion>", methods=['GET'])
def populate(emotion):
    if emotion == 'sad':
        up = 2
        low = 1
        user = 1
    elif emotion == 'happy':
        up = 1
        low = 0
        user = 2
    start_date = date(2015, 1, 1)
    end_date = date(2020, 8, 1)

    for single_date in daterange(start_date, end_date):
        post = Mood(user_id=user, rating=random.randint(low,up), time_stamp=single_date)
        db.session.add(post)
        db.session.commit()
    return render_template('home.html')

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@app.route("/cleanup", methods=['GET'])
def cleanup():
    db.session.execute(Mood.delete())
    db.session.commit()
    return render_template('home.html')