import hashlib
import json
import os
import sqlite3
from collections import defaultdict

import bottle
from beaker.middleware import SessionMiddleware
from bottle import request, template
from bottle import static_file, url
from cork import Cork
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from master import *
from utilities import compaign_config, flow_config, mesure_config, metric

bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))

db_path = 'data.db'
app = bottle.default_app()
wsock = None

is_authenticate = False

aaa = Cork('/var/lib/shinken/modules/pcd/views')

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = SessionMiddleware(app, session_opts)


# #  Bottle methods  # #
def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


# ************************************************************ WEBSOCKET
@bottle.route('/websocket')
def handle_websocket():
    global wsock
    print "hello"
    wsock = request.environ.get('wsgi.websocket')
    while True:
        wsock.receive()
        wsock.send('message')


#************************************************************ SAVE COMPAIGN CONFIG TO DATABASE
def save_compaign_config(c):
	con = sqlite3.connect(db_path)
	con.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
	compaign_name = c.name
	flows = c.flows

	con.execute('insert into compaigns(compaign_id) values (?)', (compaign_name,))

	for f in flows:
		con.execute(
			"""
			insert into flows (flow_id, source, destination, protocol, ps, ps_distro, idt, idt_distro, trans_duration, sampling_interval, compaign_id)
			values (?,?,?,?,?,?,?,?,?,?,?)
			""", (f.flow_id, 
			f.source, 
			f.destination, 
			f.protocol, 
			f.ps, f.ps_distro, 
			f.idt, f.idt_distro, 
			f.trans_duration, 
			f.sampling_interval,
			compaign_name)
		)

		for metric in f.mesure:
			con.execute('insert into metrics (flow_id, metric_name) values (?,?)', (f.flow_id, metric))


	con.commit()
	con.close()

"""def load_compaign_config(name):
	con = sqlite3.connect(db_path)
	query = "select * from compaigns, flows where compaigns.compaign_id = flows.compaign_id and compaigns.compaign_id = {}".format(name)

	rows = cn.execute(query)
	if not rows return None
	compaign = compaign_config()
	for (c_id, f_id, src, dest, prot, ps, ps_dist, idt, idt_dist, trans_dur,) in rows:"""



#************************************************************ LOAD COMPAIGN NAMES FROM DATABASE
@bottle.route('/load_past_compaigns', method='get')
def load_compaigns():
	print 'load_compaigns invoked'
	con = sqlite3.connect(db_path)
	query = 'select compaign_id from compaigns'
	rows = con.execute(query).fetchall()
	result = {'compaigns' : [comp for (comp,) in rows]}
	print result
	return json.dumps(result)



#************************************************************ POST COMPAIGN CONFIG 														
@bottle.route('/start_compaign', method='post')
def post_config():
    try:
        compaign_json = request.json
    except Exception as e:
        print 'something bad happened' + str(e)
        return
    compaign = compaign_config([])
    flows = compaign_json['compaign']
    compaign.name = compaign_json['name']

    for f in flows:
        flow = flow_config()
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
        flow.ps.append(temp['packet_size'])
        flow.ps_distro = temp['ps_distro'] if temp.has_key('ps_distro') else '-c'
        flow.idt.append(temp['rate'])
        flow.idt_distro = temp['idt_distro'] if temp.has_key('idt_distro') else '-C'
        flow.trans_duration = int(temp['trans_duration'])
        mesure = mesure_config()
        mesure.metrics.extend(temp['metrics'])
        mesure.sampling_interval = int(temp['sampling_interval'])
        flow.mesure = mesure
        compaign.add_flow(flow)

    sender = ''
    receiver = ''

    master = Master()
    print compaign.is_multicast
    results = master.post_compaign_config(compaign)
    global wsock
    json_results = defaultdict(list)
    for r in results:
        for f in compaign.flows:
            if r.flow_id == f.flow_id:
                sender = f.source
                receiver = f.destination
        print sender + "    " + receiver
        for metric in r.metrics:
            AxeX = [x for x, y in metric.values.iteritems()]
            AxeY = [y for x, y in metric.values.iteritems()]
            json_results[r.flow_id].append(
                {'flow_id': r.flow_id, 'name': metric.name, 'AxeX': AxeX, 'AxeY': AxeY, "sender": sender,
                 "receiver": receiver});

    wsock.send(json.dumps(json_results))


#************************************************************ SEND JSON DATA
@bottle.route('/test')
def test():
    global wsock
    if wsock:
        r = metric()
        r.name = 'jitter'
        r.values = {0.0: 1.5e-05, 1.0: 1.5e-05, 2.0: 1.4e-05, 3.0: 2.3e-05, 4.0: 1.3e-05, 5.0: 1.2e-05, 6.0: 1.7e-05,
                    7.0: 1.8e-05, 8.0: 1e-05, 9.0: 1.7e-05, 10.0: 1.2e-05, 11.0: 1.3e-05, 12.0: 1.4e-05, 13.0: 1.1e-05,
                    14.0: 1.6e-05}
        AxeX = [x for x, y in r.values.iteritems()]
        AxeY = [y for x, y in r.values.iteritems()]
        wsock.send(json.dumps({'name': r.name, 'AxeX': AxeX, 'AxeY': AxeY, 'data': r.values, 'con': 'con'}))
    else:
        print 'wsock is not'

#************************************************************ GET INDEX PAGE


@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/')


@bottle.route('/', method='get')
def index():
    return template('index.tpl', url=url)


@bottle.route('/', method='post')
def index():
    username = post_get('login')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/start_compaign', fail_redirect='/')


@bottle.route('/load_configs')
def index():
	''' return past configs '''
	infile = open('compaigns', 'r')
	data = infile.readlines()
	return json.dumps(data)


@bottle.route("/start_compaign")
def index():
    aaa.require(role='admin', fixed_role=True, fail_redirect='/')
    return template("index_1.tpl", url=url)


@bottle.route('/check_compaign', method='post')
def check_compaing_name():
	print 'CHECK HAS BEEN CALLED'
	data = request.json
	print data
	compaign_name = data['name']
	print 'CHECKING COMPAIGN NAME: ' + compaign_name
	con = sqlite3.connect(db_path)
	row = con.execute('select * from compaigns where compaign_id = ?', (compaign_name,)).fetchone()
	result = 'false'
	if row: result = 'true'
	check_result = {'result' : result}
	return json.dumps(check_result)

	return json.dumps(check_result)


@bottle.route('/static/<filename>', name='static')
def static(filename):
    return static_file(filename, root='static')


#************************************************************ SERVE 
server = WSGIServer(("0.0.0.0", 8081), app,
                    handler_class=WebSocketHandler)

server.serve_forever()
