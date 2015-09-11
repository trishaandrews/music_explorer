from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from wtforms import TextField, Form
from  sqlalchemy.sql.expression import func, select
import json

from musicapp.database import db_session, Recs

LIMIT = 10 #change html description p if you change this

app = Flask(__name__)

cluster_inputs = []


class SearchForm(Form):
    autocomp= TextField('autocomp',id='autocomplete')


@app.route('/autocomplete')
def autocomplete():
    db_vals = []
    search = request.args.get('search[term]')
    #app.logger.debug(search)
    db_vals += db_session.query(Recs).filter(Recs.artist.ilike('%' + search + '%')).all()
    db_vals += db_session.query(Recs).filter(Recs.title.ilike('%' + search + '%')).all() 
    results = []
    for v in db_vals[:LIMIT]:
        results.append({"value": "%s, %s" %(v.artist, v.title), 
                        "id" : v.track_id,
                        "cluster" : v.cluster})
    return Response(json.dumps(results))
    
def get_recs():
    if len(cluster_inputs) < 1:
        lim = 0
    else:
        lim = int(LIMIT/len(cluster_inputs))
    db_vals = []
    for c in cluster_inputs:
        db_vals += db_session.query(Recs).filter(Recs.cluster==c,
                   Recs.recommend==1).order_by(func.random()).limit(lim) #random selection for postgres
    results = []
    for v in db_vals:
        results.append({"value": "%s, %s" %(v.artist, v.title), 
                        "id" : v.track_id,
                        "cluster" : v.cluster})
    return results
    
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    form_vals = request.form
    app.logger.debug(form_vals)
    cluster = form_vals.get('cluster')
    cluster_inputs.append(cluster)
    results = get_recs()
    app.logger.debug(results)
    return Response(json.dumps(results))
    
@app.route('/refresh_recs', methods=['GET', 'POST'])
def refresh_recs():
    results = get_recs()
    return Response(json.dumps(results))
    
@app.route('/')
def index():
    global cluster_inputs
    cluster_inputs = []
    form = SearchForm(request.form)
    return render_template('index.html', form=form)
 
    
#if __name__ == '__main__':
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host='0.0.0.0', port=port)
