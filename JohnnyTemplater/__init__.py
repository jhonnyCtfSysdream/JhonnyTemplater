from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import current_user
from ...models import Post, Plugin
from ... import db


def new_post():
    plugin = Plugin.query.filter_by(name="JohnnyTemplater").first()

    if request.method == "POST":
        if "submit-template" in request.form:
            theme = request.form['theme']
            if theme == "":
                theme = "Funny"
            f = open("app/texts/" + theme, 'r')
            read = f.read()
            return render_template("JohnnyTemplater/new_post.html", user=current_user, plugin=plugin, read=read)

        else:
            title = request.form.get('title')
            text = request.form.get('text')

            if not title:
                flash('Both fields are required', category='error')
            elif not text:
                flash('Both fields are required', category='error')
            else:
                post = Post(text=text, title=title, author=current_user.id)
                db.session.add(post)
                db.session.commit()

                flash('Post created!', category='success')
                return redirect(url_for('views.home'))

    return render_template('JohnnyTemplater/new_post.html', user=current_user, plugin=plugin)
