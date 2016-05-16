import multiprocessing
import os
import signal
from subprocess import Popen, PIPE, check_output

import bottle
from bottle import template
from shinken.basemodule import BaseModule
from shinken.log import logger

bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
properties = {
	'daemons' : ['arbiter'],
	'type' : 'pcd',
	'external' :True 
}


def job():
    try:
        logger.info('********** job method *********')
        proc = Popen(['python', '/var/lib/shinken/modules/pcd/server.py'], stdout=PIPE, stderr=PIPE)
        proc.communicate()
    except Exception as e:
        logger.info('job: ' + str(e))


def get_instance(plugin):
    logger.info('[PCD Module broker] YO !!!!!')
    instance = pcd_module_class(plugin)
    return instance



class pcd_module_class(BaseModule):
    def __init__(self, modconf):
        self.master = None
        self.proc = None
        BaseModule.__init__(self, modconf)

    def init(self):
        logger.info('[PCD Module] init method')

    def hook_early_configuration(self, arb):
        logger.info('************** HOOK EARLY CONFIG CALLED **************')
        fh = open('/etc/shinken/h', 'w')
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

    def terminate(self):
        try:
            if self.proc:
                pass
            if self.proc:
                self.proc.terminate()
            ps = Popen(('ps', '-ef'), stdout=PIPE)
            output = check_output(('grep', '[s]erver.py'), stdin=ps.stdout)
            ps.wait()
            server_pid = output.split()[1]
            if server_pid:
                Popen(('kill', server_pid), stdout=PIPE)
                ps.wait()
            os.kill(int(server_pid), signal.SIGTERM)
        except:
            pass

    def main(self):
        try:
            proc = multiprocessing.Process(target=job)
            proc.start()
            proc.join()
        except Exception as e:
            logger.info('main: ' + str(e))

    def do_stop(self):
        logger.info('********* before leaving *********')
        try:
            ps = Popen(('ps', '-ef'), stdout=PIPE)
            output = check_output(('grep', '[s]erver.py'), stdin=ps.stdout)
            ps.wait()
            logger.info(output)
            server_pid = output.split()[1]
            if server_pid:
                logger.info('pid : ' + server_pid)
                Popen(('kill', '-9', server_pid), stdout=PIPE)
                ps.wait()
        except Exception as e:
            logger.info('stop_process: ' + str(e))
        super(pcd_module_class, self).do_stop()

    def stop_process(self):
        logger.info('********* before leaving stop_process *********')
        try:
            server_pid = None
            ps = Popen(('ps', '-ef'), stdout=PIPE)
            output = check_output(('grep', '[s]erver.py'), stdin=ps.stdout)
            ps.wait()
            logger.info(output)
            server_pid = output.split()[1]
            if server_pid:
                logger.info('pid : ' + server_pid)
                Popen(('kill', '-9', server_pid), stdout=PIPE)
                ps.wait()
        except Exception as e:
            logger.info('stop_process: ' + str(e))
        super(pcd_module_class, self).stop_process()
