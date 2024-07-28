from flask import Flask, request
from flask import render_template, current_app
from main import app as app
from application.jobs import tasks
from flask_mail import Mail, Message

# @app.route("/", methods=["GET"])
# def main():
#     return render_template("homepage.html")

@app.route("/hello", methods=["GET","POST"])
def hello():
    job = tasks.just_say_hello.delay("World")
    return str(job), 200


@app.route('/mailme',methods=['GET'])
def send_email_mine():
    msg = Message('Hello', recipients=['arnavkohli321@gmail.com'])
    current_app.extensions['mail'].send(msg)
    return 'Sent', 200
