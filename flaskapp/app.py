from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from wtforms import TextField, Form
from  sqlalchemy.sql.expression import func, select
import json

from database import db_session, Recs



app = Flask(__name__)

cluster_inputs = []

class SearchForm(Form):
    autocomp= TextField('autocomp',id='autocomplete')

@app.route('/autocomplete')
def autocomplete():
    db_vals = []
    #app.logger.debug(request.args)
    search = request.args.get('search[term]')
    #app.logger.debug(search)
    db_vals += db_session.query(Recs).filter(Recs.title.ilike('%' + search + '%')).all() 
    #.limit(10orwhatever)
    db_vals += db_session.query(Recs).filter(Recs.artist.ilike('%' + search + '%')).all()
    results = []
    for v in db_vals[:10]:
        results.append({"value": "%s, %s" %(v.artist, v.title), 
                        "id" : v.track_id,
                        "cluster" : v.cluster})
    #app.logger.debug(db_vals)
    #app.logger.debug(json.dumps(results))
    return Response(json.dumps(results))
    
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    global cluster_inputs
    form_vals = request.form
    app.logger.debug(form_vals)
    cluster = form_vals.get('cluster')
    cluster_inputs.append(cluster)
    app.logger.debug(len(cluster_inputs))
    n = int(12/len(cluster_inputs))
    app.logger.debug(n)
    #entries.append({"text": form_vals.get('label')})
    db_vals = []
    for c in cluster_inputs:
        db_vals += db_session.query(Recs).filter(Recs.cluster==c, Recs.recommend==1).order_by(func.random()).limit(n) #random selection for postgres
    results = []
    for v in db_vals:
        results.append({"value": "%s, %s" %(v.artist, v.title), 
                        "id" : v.track_id,
                        "cluster" : v.cluster})
    app.logger.debug(results)
    return Response(json.dumps(results))
    
@app.route('/')
def index():
    global cluster_inputs
    cluster_inputs = []
    app.logger.debug("cl_in " + str(len(cluster_inputs)))
    form = SearchForm(request.form)
    return render_template('index.html', form=form)
    
if __name__ == '__main__':
    app.debug = True
    app.run()
