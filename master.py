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

SerializerBase.register_class_to_dict(flow_config, flow_config_class_to_dict)
SerializerBase.register_dict_to_class("flow_config", flow_config_dict_to_class)

SerializerBase.register_class_to_dict(mesure_config, mesure_config_class_to_dict)
SerializerBase.register_dict_to_class("mesure_config", mesure_config_dict_to_class)


class Master(object):
    def __init__(self):
        self.pending_compaigns = []
        self.pending_flow_results = []
        self.results = []
        self.current_senders = []
        self.current_receivers = []

    def post_compaign_config(self, config):
        if self.has_pending_compaigns(): return
        self.pending_compaigns.append(config)
        result_check = self.check_hosts_availability(config.get_senders(), config.get_receivers())

        if result_check == True:
            for sender in self.current_senders:
                result = sender.start_compaign()
                print result
                # TODO: creer un processus pour chaque sender
                # TODO: traiter l'erreur dans le cas de l'echec de start_compaign

    def check_hosts_availability(self, senders, receivers):
        ''' Internal method to check hosts
			for remote objects '''
        unreach_senders = []
        unreach_receivers = []

        for sender in senders:
            try:
                s = Pyro4.Proxy('PYRO:' + sender + '_sender@' + sender + ':45000')
                if not s.setup_compaign(self.pending_compaigns[0].get_flows_by_sender(sender), "127.0.0.1"):
                    unreach_senders.append(sender)
                else:
                    self.current_senders.append(s)
            except Exception as e:
                print  "check senders " + str(e.message)
                unreach_senders.append(sender)

        for recv in receivers:
            try:
                r = Pyro4.Proxy('PYRO:' + recv + '_receiver@' + recv + ':45000')
                result_check = r.check_requirments()
                if not result_check:
                    unreach_receivers.append(recv)
                elif result_check == 'server is already running':
                    print result_check
                # TODO: traiter le cas de "server is running"
                else:
                    self.current_receivers.append(r)
            except:
                unreach_receivers.append(recv)
        print self.current_receivers
        print self.current_senders
        if not unreach_senders and not unreach_receivers:
            return True
        else:
            return False

            # process check results
            # TODO : traiter le cas ou il y a des senders ou receivers inaccessibes

    def has_pending_compaigns(self):
        return len(self.pending_compaigns)

    def post_result(self, result):
        ''' A sender uses this method to deposit a result '''

        if result.flow_id in self.pending_flow_results:
            self.pending_flow_results.remove(result.flow_id)
            self.results.append(result)

    def basic_ping(self):
        return 'master working'  # test purpose only

    def call_sender(self, sender_ip):
        s = Pyro4.Proxy('PYRONAME:' + sender_ip + '_sender')
        s.basic_ping()


def main():
    master = Master()
    #	config_file = open('file.cfg', 'r')
    #	ip = config_file.read(15)
    #	master_name = ip.strip() + '_master'

    Pyro4.Daemon.serveSimple(
        {
            master: 'master'
        },
        # host=ip,
        ns=True
    )


if __name__ == '__main__':
    master = Master()
    f = flow_config()
    f.idt = "fsf"
    f.protocol = Protocols.tcp
    m = mesure_config()
    m.sampling_interval = 1
    m.metrics.extend([Metrics.jitter, Metrics.packet_loss, Metrics.delay, Metrics.bit_rate])
    f.mesure = m
    config = compaign_config([f])
    master.post_compaign_config(config)
