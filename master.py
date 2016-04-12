import Pyro4

from serialization import *


class Master(object):
    def __init__(self):
        self.pending_compaigns = []
        self.pending_flow_results = []
        self.results = []
        self.current_senders = []
        self.current_receivers = []
        self.unreach_senders = []
        self.unreach_receivers = []

    def post_compaign_config(self, config):
        if self.has_pending_compaigns():
            return
        self.pending_compaigns.append(config)
        result_check = self.check_hosts_availability(config.get_senders(), config.get_receivers())
        if result_check:
            for sender in self.current_senders:
                result = sender.start_compaign()
                print result.flow_id
                self.pending_compaigns.remove(config)
                # TODO: creer un processus pour chaque sender
                # TODO: traiter l'erreur dans le cas de l'echec de start_compaign

    def check_hosts_availability(self, senders, receivers):
        ''' Internal method to check hosts
			for remote objects '''
        for sender in senders:
            try:
                s = Pyro4.Proxy('PYRO:' + sender + '_sender@' + sender + ':45000')
                if not s.setup_compaign(self.pending_compaigns[0].get_flows_by_sender(sender), "127.0.0.1"):
                    self.unreach_senders.append(sender)
                else:
                    self.current_senders.append(s)
            except Exception as e:
                print "check senders " + str(e.message)
                self.uself.nreach_senders.append(sender)

        for recv in receivers:
            try:
                r = Pyro4.Proxy('PYRO:' + recv + '_receiver@' + recv + ':45000')
                result_check = r.check_requirments()
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
    f.protocol = Protocols.tcp
    f.idt_distro = Idt_disto.constant
    f.idt.append(1500)
    f.ps.append(512)
    f.ps_distro = Ps_distro.constant
    m = mesure_config()
    m.sampling_interval = 1
    m.metrics.extend([Metrics.jitter, Metrics.packet_loss, Metrics.delay, Metrics.bit_rate])
    f.mesure = m

    '''f1 = flow_config()
    f1.protocol = Protocols.udp
    f1.idt_distro = Idt_disto.constant
    f1.idt.append(1200)
    f1.ps.append(488)
    f1.ps_distro = Ps_distro.constant
    m1 = mesure_config()
    m1.sampling_interval = 1
    m1.metrics.extend([Metrics.jitter, Metrics.packet_loss, Metrics.delay, Metrics.bit_rate])
    f1.mesure = m1'''

    config = compaign_config([f])
    master.post_compaign_config(config)
