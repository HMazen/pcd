import multiprocessing

import Pyro4

from serialization import *


def job(obj, liste):
    try:
        result = obj.start_compaign()
        print result
        for r in result:
            liste.append(r.flow_id)
            liste.append(r.metrics[0].values)
    except Exception as e:
        print "jobs ", str(e)

class Master(object):
    def __init__(self):
        self.pending_compaign = None
        self.pending_flow_results = []
        self.current_processes = []
        self.current_senders = []
        self.current_receivers = []
        self.unreach_senders = []
        self.unreach_receivers = []
        self.results = []

    def post_compaign_config(self, config):
        if self.pending_compaign:
            return
        self.pending_compaigns = config
        result_check = self.check_hosts_availability(config.get_senders(), config.get_receivers(),
                                                     self.pending_compaigns.is_multicast)
        if result_check:
            self.results = multiprocessing.Manager().list()
            for sender in self.current_senders:
                proc = multiprocessing.Process(target=job, args=(sender, self.results))
                proc.start()
                self.current_processes.append(proc)
            for proc in self.current_processes:
                proc.join()
            for r in self.current_receivers:
                r.terminate_proc()
            print self.results
        self.pending_compaigns = None
        del self.current_receivers[:]
        del self.current_senders[:]
        del self.current_processes[:]
        # TODO: traiter l'erreur dans le cas de l'echec de start_compaign

    def check_hosts_availability(self, senders, receivers, is_multicast):
        ''' Internal method to check hosts
        for remote objects '''
        for sender in senders:
            try:
                s = Pyro4.Proxy('PYRO:' + sender + '_sender@' + sender + ':45000')
                if not s.setup_compaign(self.pending_compaigns.get_flows_by_sender(sender), is_multicast):
                    self.unreach_senders.append(sender)
                else:
                    self.current_senders.append(s)
            except Exception as e:
                print "check senders " + str(e.message)
                self.unreach_senders.append(sender)

        for recv in receivers:
            try:
                r = Pyro4.Proxy('PYRO:' + recv + '_receiver@' + recv + ':45000')
                result_check = r.check_requirments(is_multicast)
                if not result_check:
                    self.unreach_receivers.append(recv)
                elif result_check == 'server is already running':
                    print result_check
                # TODO: traiter le cas de "server is running"
                else:
                    self.current_receivers.append(r)
            except:
                self.unreach_receivers.append(recv)
        print self.current_receivers
        print self.current_senders
        if not self.unreach_senders and not self.unreach_receivers:
            return True
        else:
            return False

            # process check results
            # TODO : traiter le cas ou il y a des senders ou receivers inaccessibes

    def post_result(self, result):
        ''' A sender uses this method to deposit a result '''
        if result.flow_id in self.pending_flow_results:
            self.pending_flow_results.remove(result.flow_id)
            self.results.append(result)

    def basic_ping(self):
        return 'master working'  # test purpose only


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
    f.protocol = Protocols.tcp
    f.idt_distro = Idt_disto.constant
    f.idt.append(1500)
    f.ps.append(512)
    f.ps_distro = Ps_distro.constant
    m = mesure_config()
    m.sampling_interval = 1
    m.metrics.extend([Metrics.jitter, Metrics.packet_loss, Metrics.delay, Metrics.bit_rate])
    f.mesure = m
    f.source = "192.168.56.1"
    f.destination = "192.168.56.1"


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
