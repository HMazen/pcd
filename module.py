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

app = bottle.Bottle()


def get_instance(plugin):
	logger.info('[PCD Module broker] YO !!!!!')
	instance = pcd_module_class(plugin)
	app.route('/', method='GET')(instance.index)
	app.route('/', method='POST')(instance.index_post)
	return instance



class pcd_module_class(BaseModule):
	def __init__(self, modconf):
		self.master = None
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

	def index(self):
		return template('index.tpl')
	def index_post(self):
		logger.info('***** calling master *****')
		self.master.call_sender('192.168.1.5')
		logger.info('***** master called *****')

	def main(self):
		self.master = Pyro4.Proxy('PYRONAME:master')
		app.run(host='localhost', port=8080)



