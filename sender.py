from subprocess import *

from Pyro4.util import SerializerBase

from utilities import *


def flow_config_class_to_dict(obj):
    return dict(__class__="flow_config", flow_id=obj.flow_id, source=obj.source, destination=obj.destination,
                protocol=obj.protocol, ps=obj.ps, ps_distro=obj.ps_distro, idt=obj.idt, idt_distro=obj.idt_distro,
                starting_date=obj.starting_date, trans_duration=obj.trans_duration, mesure=obj.mesure)


def flow_config_dict_to_class(classname, d):
    return flow_config()


SerializerBase.register_class_to_dict(flow_config, flow_config_class_to_dict)
SerializerBase.register_dict_to_class("flow_config", flow_config_dict_to_class)


class Sender(object):
    def __init__(self):
        self.results = []
        self.master_ip = ''
        self.remote_receiver = None
        self.remote_master = None
        self.num_flows = 0
        self.current_flows = None

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
        return True

    def basic_ping(self):
        print 'sender working'  # test purpose only

    def post_result(self, result):
        ''' for the receiver to post results '''
        self.results.append(result)

    def start_compaign(self):
        for flow in self.current_flows:
            if self.check_requirments():
                command = ["iperf3", "-c"]
                out = Popen(command, stdout=PIPE, stderr=PIPE)
                (stdout, stderr) = out.communicate()

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
