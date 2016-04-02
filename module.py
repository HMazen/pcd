from shinken.basemodule import BaseModule
from shinken.log import logger
from bottle import request, response, template, route, view
from master import Master
import Pyro4
import bottle
import os
bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
properties = {
	'daemons' : ['arbiter'],
	'type' : 'pcd',
	'external' :True 
}



def get_instance(plugin):
	logger.info('[PCD Module broker] YO !!!!!')
	instance = pcd_module_class(plugin)
	return instance

app = bottle.Bottle()


class pcd_module_class(BaseModule):
	def __init__(self, modconf):
		BaseModule.__init__(self, modconf)

	def init(self):
		logger.info('[PCD Module] init method')

	def hook_early_configuration(self, arb):
		logger.info('************** HOOK EARLY CONFIG CALLED **************')
		fh =open('/etc/shinken/h', 'w')
		for h in arb.conf.hosts:
			if not hasattr(h, 'address') and not hasattr(h, 'host_name'):
                		continue
			addr = None

            		# By default take the address, if not, take host_name
            		if not hasattr(h, 'address'):
                		addr = h.host_name
            		else:
                		addr = h.address
			fh.write(h.get_name() + ': ' + addr + '\n')
		fh.close()

	@app.route("/",method = "GET")
	def index():
		return template('index.tpl')
	@app.route("/",method = "POST")
	def index_post():
		s = request.forms.get('source')
		d = request.forms.get('destination')
		logger.info('***********' + s + '	'+d+'**********')

	def main(self):
		app.run(host='localhost', port=8080)



