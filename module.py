import os
from subprocess import Popen, PIPE

import bottle
from shinken.basemodule import BaseModule
from shinken.log import logger

bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
properties = {
	'daemons' : ['arbiter'],
	'type' : 'pcd',
	'external' :True 
}


def job():
    str = ""
    err = ""
    try:
        logger.info('********** job method *********')
        p = Popen(['python', '/var/lib/shinken/modules/pcd/server.py'], stdout=PIPE, stderr=PIPE)
        out = p.stdout.readline()
        while True:
            if out:
                logger.info("---------------------------" + out)
            out = p.stdout.readline()
        (str, err) = p.communicate()
        logger.info("---------------------------" + str + "     " + err)
    except Exception as e:
        logger.info('job: ' + str(e))
        logger.info("||||||||||||||||||||||" + str + "     " + err)


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
        try:
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
        except Exception as e:
            logger.info('hook_early_config: ' + str(e))


    def main(self):
        try:
            pass
        except Exception as e:
            logger.info('main: ' + str(e))

