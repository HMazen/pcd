from subprocess import *

import Pyro4
from Pyro4.util import SerializerBase

from utilities import *


def flow_config_class_to_dict(obj):
    return dict(__class__="flow_config", flow_id=obj.flow_id, source=obj.source, destination=obj.destination,
                protocol=obj.protocol, ps=obj.ps, ps_distro=obj.ps_distro, idt=obj.idt, idt_distro=obj.idt_distro,
                starting_date=obj.starting_date, trans_duration=obj.trans_duration,
                mesure=obj.mesure)

def flow_config_dict_to_class(classname, d):
    f = flow_config()
    f.flow_id = d["flow_id"]
    f.source = d["source"]
    f.destination = d["destination"]
    f.idt = d["idt"]
    f.idt_distro = d["idt_distro"]
    f.ps = d["ps"]
    f.ps_distro = d["ps_distro"]
    f.protocol = d["protocol"]
    f.starting_date = d["starting_date"]
    f.trans_duration = d["trans_duration"]
    f.mesure = d["mesure"]
    m = mesure_config()
    m.metrics = d["mesure"]["metrics"]
    m.sampling_interval = d["mesure"]["sampling_interval"]
    m.finish_date = d["mesure"]["finish_date"]
    m.start_date = d["mesure"]["start_date"]
    f.mesure = m
    return f

SerializerBase.register_class_to_dict(flow_config, flow_config_class_to_dict)
SerializerBase.register_dict_to_class("flow_config", flow_config_dict_to_class)


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


class Sender(object):
    def __init__(self):
        self.results = []
        self.master_ip = ''
        self.remote_receiver = None
        self.remote_master = None
        self.num_flows = 0
        self.current_flows = None
        self.current_mesures = None

    def setup_compaign(self, flows, master_ip):
        # setup the communication with the master
        if not self.master_ip:
            self.master_ip = master_ip
        if not self.remote_master:
            try:
                # self.remote_master = self.get_remote_master()
                pass
            except:
                pass
                # TODO: handle exception

        # check traffic generation requirments
        result_check = self.check_requirments()
        if not result_check:
            return result_check
        self.current_flows = flows
        print self.current_flows[0]
        print self.current_flows[0].mesure.sampling_interval
        # self.current_mesures = mesures
        return True

    def basic_ping(self):
        print 'sender working'  # test purpose only

    def post_result(self, result):
        ''' for the receiver to post results '''
        self.results.append(result)

    def start_compaign(self):
        for flow in self.current_flows:
            if self.check_requirments():
                command = ["ITGSend", "-a", flow.destination, "-x", "logfile", "-T", flow.protocol]
                out = Popen(command, stdout=PIPE, stderr=PIPE)
                (stdout, stderr) = out.communicate()
                print 'PYRO:' + flow.destination + '_receiver@' + flow.destination + ':45000'
                r = Pyro4.Proxy('PYRO:' + flow.destination + '_receiver@' + flow.destination + ':45000')
                result = r.get_result(flow.mesure)
                print result
                return result
                # TODO: verifier le fonctionnement de iperf et d-itg et ecrire les flows dans un fichier

    def check_requirments(self):
        try:
            command = ["iperf3", "-v"]
            out = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = out.communicate()

            command = ["ITGSend", "-h"]
            out = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = out.communicate()
            return True
        except:
            return False

    def print_result(self, r):
        print r
