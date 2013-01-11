import json
import os
from StringIO import StringIO
from tempfile import NamedTemporaryFile, TemporaryFile
from dataconverters import csv, xls
import requests
from werkzeug import secure_filename
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
    metadata = request.args.to_dict()
    # Error checking
    url = request.args.get('url', None)
    originformat = request.args.get('type', None)
    if url is None:
        return error('No URL given')
    if targetformat is None or originformat is None:
        return error('No format or type specified')
    module = converters.get(originformat, None)
    if module is None:
        return error('No converter found for {0}',format(originformat))

    # Fetch the url
    r = requests.get(url)
    if requests.codes.ok != r.status_code:
        return error("Could't access the file at {0}".format(url))
    handle = StringIO(r.content)
    try:
        results, metadata = module.parse(handle, **metadata)
        results_json = json.dumps({'metadata': metadata, 'records': list(results)}, cls=IteratorEncoder)
    except Exception as e:
        return error(str(e))
    return Response(results_json, mimetype='application/json')

"""
@app.route('/api/convert/<targetformat>', methods=['POST'])
@crossdomain(origin='*', headers=cors_headers)
@jsonpify
def convert_post(targetformat=None):
    uploaded_file = request.files['file']
    metadata = request.form.to_dict()
    results = {}
    metadata['target'] = targetformat
    if not uploaded_file or targetformat is None:
        results['error'] = 'No file uploaded or format specified'
        results_json = json.dumps(results)
        return Response(results_json, mimetype='application/json')
    metadata['mime_type'] = uploaded_file.content_type
    try:
        data = dataconverter(uploaded_file.stream, metadata)
        header, results = data.convert()
        results_json = json.dumps({'headers': header, 'data': results})
    except Exception as e:
        results['error'] = str(e)
        results_json = json.dumps(results)
    return Response(results_json, mimetype='application/json')
"""
