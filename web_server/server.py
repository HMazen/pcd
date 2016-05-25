import hashlib
import json
import os
import sys
from collections import defaultdict

import pam
from flask import Flask, request, session, redirect, url_for, render_template
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

sys.path.append("/var/lib/shinken/modules/pcd/")
from managed_daemon import master, utilities

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True
host, port = 'localhost', 5000

wsock = None


@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response




def wsgi_app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        return app(environ, start_response)
    elif path == "/websocket":
        handle_websocket(environ["wsgi.websocket"])
    else:
        return app(environ, start_response)


def handle_websocket(ws):
    global wsock
    wsock = ws
    while True:
        message = ws.receive()
        if message is None:
            break


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        p = pam.pam()
        if p.authenticate(request.form['username'], request.form['password']):
            session['logged_in'] = True
            return redirect(url_for('start_compaign'))
    return render_template('index.html', error='invalid username/password')


@app.route('/start_compaign')
def start_compaign():
    ipaddresses = []
    try:
        with open('/var/lib/shinken/modules/pcd/ipaddresses', 'r') as fh:
            ipaddresses = fh.readlines()
    except:
        pass
    if session.get('logged_in'):
        return render_template('start_compaign.html', ips=ipaddresses)
    return render_template('index.html', error='you must login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/send_config', methods=['POST'])
def send_config():
    try:
        if not session.get('logged_in'):
            return render_template('index.html', error='you must login')
        compaign_json = request.json
        print compaign_json
    except Exception as e:
        print 'something bad happened' + str(e)
        return
    compaign = utilities.compaign_config([])
    flows = compaign_json['compaign']
    compaign.name = compaign_json['name']

    for f in flows:
        flow = utilities.flow_config()
        temp = json.loads(f)
        print 'flow id before encoding: ' + temp['date']
        flow.flow_id = hashlib.md5(temp['date']).hexdigest()
        print 'flow id after encoding: ' + flow.flow_id
        flow.source = temp['source_ip']
        flow.destination = temp['destination_ip']
        flow.protocol = temp['protocol']
        if flow.protocol == "Multicast":
            flow.protocol = "UDP"
            compaign.is_multicast = True

        ps_distro = '-c'
        ps_means = {}
        for k, v in temp['ps_params'].iteritems():
            if k == "Poisson":
                ps_distro = '-o'
            elif k == "Exponential":
                ps_distro = '-e'
            elif k == "Uniform":
                ps_distro = '-u'
            elif k == "Gamma":
                ps_distro = '-g'
            elif k == "Cauchy":
                ps_distro = '-y'
            elif k == "Weibull":
                ps_distro = '-w'
            elif k == "Pareto":
                ps_distro = '-v'
            elif k == "Normal":
                ps_distro = '-n'
            ps_means = v

        flow.ps_distro = ps_distro

        idt_distro = '-C'
        idt_means = {}
        for k, v in temp['idt_params'].iteritems():
            if k == "Poisson":
                idt_distro = '-O'
            elif k == "Exponential":
                idt_distro = '-E'
            elif k == "Uniform":
                idt_distro = '-U'
            elif k == "Gamma":
                idt_distro = '-G'
            elif k == "Cauchy":
                idt_distro = '-Y'
            elif k == "Weibull":
                idt_distro = '-W'
            elif k == "Pareto":
                idt_distro = '-V'
            elif k == "Normal":
                idt_distro = '-N'
            idt_means = v

        flow.idt_distro = idt_distro
        if flow.ps_distro != "-c":
            for k, v in ps_means.iteritems():
                flow.ps.append(v)
        else:
            flow.ps.append(temp["ps_params"]["Constant"])

        if flow.idt_distro != "-C":
            for k, v in idt_means.iteritems():
                flow.idt.append(v)
        else:
            flow.idt.append(temp["idt_params"]["Constant"])

        flow.trans_duration = int(temp['trans_duration'])
        mesure = utilities.mesure_config()
        mesure.metrics.extend(temp['metrics'])
        mesure.sampling_interval = int(temp['sampling_interval'])
        flow.mesure = mesure

        compaign.add_flow(flow)

    sender = ''
    receiver = ''

    m = master.Master()
    results = m.post_compaign_config(compaign)

    global wsock

    json_results = defaultdict(list)
    for r in results:
        for f in compaign.flows:
            if r.flow_id == f.flow_id:
                sender = f.source
                receiver = f.destination

        for metric in r.metrics:
            unit = ''
            if metric.name == "bit rate":
                unit = 'Kbit/s'
            elif metric.name == "packet loss":
                unit = 'pkt'
            else:
                unit = 's'

            AxeX = [x for x, y in metric.values.iteritems()]
            AxeY = [y for x, y in metric.values.iteritems()]
            json_results[r.flow_id].append(
                {'flow_id': r.flow_id, 'name': metric.name, 'AxeX': AxeX, 'AxeY': AxeY, "sender": sender,
                 "receiver": receiver, "unit": unit})
    wsock.send(json.dumps(json_results))
    return 'OK'


if __name__ == '__main__':
    http_server = WSGIServer((host, port), wsgi_app, handler_class=WebSocketHandler)
    print('Server started at %s:%s' % (host, port))
    http_server.serve_forever()
