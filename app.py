import sqlite3
from datetime import date, datetime as dt
from flask import Flask,render_template,request,jsonify
from pytz import timezone
from werkzeug.exceptions import abort


app = Flask(__name__)

class Season:
    def __init__(self, id, start_date,end_date,description):
        self.id=id
        self.start_date = str(dt.strptime(start_date,'%Y-%m-%d').month)+'/'+str(dt.strptime(start_date,'%Y-%m-%d').day)
        self.end_date = str(dt.strptime(end_date,'%Y-%m-%d').month)+'/'+str(dt.strptime(end_date,'%Y-%m-%d').day)
        self.description=description
        self.image="./static/assets/img_"+str(self.id)+".jpg"
        self.dictionary={'id':self.id,'start_date':self.start_date,'end_date':self.end_date,'description':self.description,'image':self.image}

@app.route('/')
def index():
    conn = get_db_connection()
    ms = conn.execute('SELECT rowid,* FROM microseasons').fetchall()
    microseasons=[]
    for s in ms:
        seasons=Season(s['rowid'],s['start_date'],s['end_date'],s['description'])
        microseasons.append(seasons)
    s=get_season_from_date(dt.now(timezone('US/Eastern')))
    season=Season(s['rowid'],s['start_date'],s['end_date'],s['description'])
    conn.close()
    return render_template('index.html',seasons=microseasons,season=season)


@app.route('/get',methods=['GET'])
def season():
    id=request.args.get('id')
    s=get_season_from_id(id)
    season=Season(s['rowid'],s['start_date'],s['end_date'],s['description'])
    return jsonify(season.dictionary)

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