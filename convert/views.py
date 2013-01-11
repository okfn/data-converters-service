import json
from StringIO import StringIO
from dataconverters import csv, xls
import requests
from flask import request, render_template, Response
from convert import app
from convert.util import crossdomain, error, IteratorEncoder, jsonpify


cors_headers = ['Content-Type', 'Authorization']
converters = dict(csv=csv, xls=xls)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/convert/<targetformat>', methods=['GET'])
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert_get(targetformat='json'):

    # Error checking
    metadata = request.args.to_dict()
    url = request.args.get('url', None)
    originformat = request.args.get('type', None)
    if url is None:
        return error('No URL given')
    if targetformat is None or originformat is None:
        return error('No format or type specified')
    module = converters.get(originformat, None)
    if module is None:
        return error('No converter found for {0}'.format(originformat))

    # Fetch the url
    r = requests.get(url)
    if requests.codes.ok != r.status_code:
        return error("Could't access the file at {0}".format(url))

    # Convert
    handle = StringIO(r.content)
    try:
        results, metadata = module.parse(handle, **metadata)
        results_json = json.dumps({'metadata': metadata, 'records': list(
                                  results)}, cls=IteratorEncoder)
    except Exception as e:
        return error(str(e))
    return Response(results_json, mimetype='application/json')


@app.route('/api/convert/<targetformat>', methods=['POST'])
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert_post(targetformat='json'):

    # Error checking
    uploaded_file = request.files['file']
    metadata = request.form.to_dict()
    originformat = request.form.get('type', None)
    if not uploaded_file:
        return error('No file given')
    if targetformat is None or originformat is None:
        return error('No format or type specified')
    module = converters.get(originformat, None)
    if module is None:
        return error('No converter found for {0}'.format(originformat))

    # Convert
    try:
        results, metadata = module.parse(uploaded_file.stream, **metadata)
        results_json = json.dumps({'metadata': metadata, 'records': list(
                                  results)}, cls=IteratorEncoder)
    except Exception as e:
        return error(str(e))
    return Response(results_json, mimetype='application/json')
