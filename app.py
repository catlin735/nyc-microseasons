import sqlite3
from datetime import date, datetime as dt
from flask import Flask,render_template,request, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

class Season:
    def __init__(self, id, start_date,end_date,description):
        self.id=id
        self.start_date = str(dt.strptime(start_date,'%Y-%m-%d').month)+'/'+str(dt.strptime(start_date,'%Y-%m-%d').day)
        self.end_date = str(dt.strptime(end_date,'%Y-%m-%d').month)+'/'+str(dt.strptime(end_date,'%Y-%m-%d').day)
        self.description=description

@app.route('/')
def index():
    return redirect("/0")

@app.route('/image')
def image():
    return "./static/assets/img_1.jpg"
@app.route('/<int:id>')
def season(id=1):
    conn = get_db_connection()
    microseasons = conn.execute('SELECT rowid FROM microseasons').fetchall()
    if id==0:
        s=get_season_from_date(dt.today())
    else:
        s=get_season_from_id(id)
    season=Season(s['rowid'],s['start_date'],s['end_date'],s['description'])
    conn.close()
    image="./static/assets/img_"+str(season.id)+".jpg"
    return render_template('index.html',seasons=microseasons,season=season,image=image)

def get_season_from_date(curr_date):
    new_date=date(2024,curr_date.month,curr_date.day)
    conn = get_db_connection()
    season = conn.execute('SELECT rowid, * FROM microseasons WHERE start_date <= ? AND end_date >= ?',
                        (new_date,new_date,)).fetchone()
    if season is None:
         season = conn.execute('SELECT rowid, * FROM microseasons WHERE rowid = ?',
                        (1,)).fetchone()
    conn.close()
    return season

def get_season_from_id(id):
    conn = get_db_connection()
    season = conn.execute('SELECT rowid, * FROM microseasons WHERE rowid = ?',
                        (id,)).fetchone()
    conn.close()
    if season is None:
        abort(404)
    return season

def get_db_connection():
    conn = sqlite3.connect('nyc_microseasons.db')
    conn.row_factory = sqlite3.Row
    return conn