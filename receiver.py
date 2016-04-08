import multiprocessing
import sys
import time
from subprocess import Popen, PIPE, check_output

from Pyro4.util import SerializerBase

from utilities import *


def mesure_config_class_to_dict(obj):
    return dict(__class__="mesure_config", metrics=obj.metrics, start_date=obj.start_date, finish_date=obj.finish_date,
                sampling_interval=obj.sampling_interval)


def mesure_config_dict_to_class(classname, d):
    m = mesure_config()
    m.metrics = d["metrics"]
    m.sampling_interval = d["sampling_interval"]
    m.finish_date = d["finish_date"]
    m.start_date = d["start_date"]
    return m


SerializerBase.register_class_to_dict(mesure_config, mesure_config_class_to_dict)
SerializerBase.register_dict_to_class("mesure_config", mesure_config_dict_to_class)


def job(command):
    try:
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        out = p.stdout.readline()
        while out:
            print out
            out = p.stdout.readline()
    except Exception as e:
        print str(e)

        sys.exit(3)


class Receiver(object):
    def __init__(self):
        self.ip_adress = ''
        self.sender_ip = ''
        self.remote_sender = None
        self.result = None
        self.proc = None

    def setup_rcv(self, source_ip):
        self.sender_ip = source_ip
        status = self.check_requirments()
        return status

    def basic_ping(self):
        print 'receiver working'  # test purpose only

    def check_requirments(self):
        try:
            command = ["ITGRecv", "-a", self.ip_adress]
            if not self.proc:
                self.proc = multiprocessing.Process(target=job, args=(command,))
                self.proc.start()
                time.sleep(1)
                if self.proc.exitcode == None:
                    return True
                else:
                    return False
            else:
                return "server is already running"
        except Exception as e:
            print str(e)
            return str(e)

    def terminate_proc(self):
        if self.proc:
            self.proc.terminate()
            ps = Popen(('ps', '-ef'), stdout=PIPE)
            output = check_output(('grep', '[I]TGRecv'), stdin=ps.stdout)
            ps.wait()
            server_pid = output.split()[1]
            if server_pid:
                Popen(('kill', server_pid), stdout=PIPE)
                ps.wait()
            self.proc = None

    def get_result(self, mesure):
        try:
            self.terminate_proc()
            print mesure.metrics
            '''ps = Popen(('ITGDec', 'logfile', '-c', str(mesure.sampling_interval*1000), 'result'), stdout=PIPE).communicate()
            with open("result") as f : s = f.read()

            return s'''
        except Exception as e:
            print str(e)
