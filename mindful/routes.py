
from flask import render_template, url_for, flash, redirect
from mindful import app, db
from flask_login import current_user
from mindful.forms import CheckIn
from mindful.models import User, Mood

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/checkin/new", methods=['GET', 'POST'])
def checkin():
    form = CheckIn()
    if form.validate_on_submit():
        if form.mood0.data == True:
            post = Mood(rating=0, author=current_user)
            pass
        if(form.mood1.data == True):
            post = Mood(rating=1, author=current_user)
            pass
        if(form.mood2.data == True):
            post = Mood(rating=2, author=current_user)
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