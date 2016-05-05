from bottle import request, post, run, get, route, template, response
from bottle import static_file, Bottle, url
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from utilities import compaign_config, flow_config
from master import Master
import json
import bottle
import sqlite3
import Pyro4
import time
import hashlib
import random
import os

bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
master = Master()

db_path = 'data.db'
app = bottle.default_app()
wsock = None


#************************************************************ WEBSOCKET 
@app.route('/websocket')
def handle_websocket():
	global wsock
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
@app.route('/load_past_compaigns', method='get')
def load_compaigns():
	print 'load_compaigns invoked'
	con = sqlite3.connect(db_path)
	query = 'select compaign_id from compaigns'
	rows = con.execute(query).fetchall()
	result = {'compaigns' : [comp for (comp,) in rows]}
	print result
	return json.dumps(result)



#************************************************************ POST COMPAIGN CONFIG 														
@app.route('/', method='post')
def post_config():
	try:
		compaign_json = request.json
	except Exception as e:
		print 'something bad happened' + str(e)
		return
	compaign = compaign_config()
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
		flow.protocol = temp['protocol'].upper()
		flow.ps = temp['packet_size']
		flow.ps_distro = temp['ps_distro'] if temp.has_key('ps_distro') else 'null'
		flow.idt = temp['idt'] 
		flow.idt_distro = temp['idt_distro'] if temp.has_key('idt_distro') else 'null'
		flow.trans_duration = temp['trans_duration']
		flow.mesure = temp['metrics']
		flow.sampling_interval = temp['sampling_interval']
		compaign.add_flow(flow)
		f1 = flow_config()
                f1.flow_id = 123
    f1.protocol = Protocols.udp
    f1.idt_distro = Idt_disto.constant
    f1.idt.append(1200)
    f1.ps.append(488)
    f1.ps_distro = Ps_distro.constant
    m1 = mesure_config()
    m1.sampling_interval = 1
    m1.metrics.extend([Metrics.jitter, Metrics.packet_loss, Metrics.delay, Metrics.bit_rate])
    f1.mesure = m1
    f1.source = "192.168.56.101"
    f1.destination = "192.168.56.102"

    config = compaign_config([f])
    config.is_multicast = True
    master.post_compaign_config(config)

	save_compaign_config(compaign)

	print compaign_json


#************************************************************ SEND JSON DATA
@app.route('/test')
def test():
	global wsock
	if wsock:
		wsock.send(json.dumps({'name' : 'bandwidth', 'data' : [random.randrange(0,100) for i in range(0,100)]}))
	else:
		print 'wsock is not'

#************************************************************ GET INDEX PAGE
@app.route('/', method='get')
def index():
	if not wsock:
		pass
	return template('index_1.tpl', url=url)

@app.route('/load_configs')
def index():
	''' return past configs '''
	infile = open('compaigns', 'r')
	data = infile.readlines()
	return json.dumps(data)


@app.route('/check_compaign', method='post')
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


@app.route('/static/<filename>', name='static')
def static(filename):
    return static_file(filename, root='static')



#************************************************************ SERVE 
server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)

server.serve_forever()
