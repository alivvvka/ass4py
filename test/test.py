from datetime import datetime, timedelta
from flask import Flask , redirect, url_for,render_template
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import requests
from bs4 import BeautifulSoup

app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lenovo2001@localhost/postgres'
db = SQLAlchemy(app)
class Example(db.Model):
    __tablename__ = 'coins'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Unicode)
    def __init__(self, id, data):
        self.id = id
        self.data = data

@app.route('/' ,methods = ["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["coin"]
        return redirect(url_for("user",usr = user))
    else:
        return render_template("form.html")

@app.route("/coin/<usr>")
def user(usr):

    url = 'https://www.google.com/search?q=site:https://coinmarketcap.com/+' + usr + '&num=20'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    i = 1
    for g in soup.find_all('h3'):
        new_ex = Example(i,g.text)
        db.session.add(new_ex)
        db.session.commit()
        i=i+1
    titles = soup.find_all('h3')
    return str(titles).replace(",", " ").replace("["," ").replace("]"," ")

        

if __name__ == '__main__':
    app.run(debug=True)
