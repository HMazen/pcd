import os
from subprocess import *

import Pyro4


class Sender(object):
    def __init__(self):
        self.results = []
        self.master_ip = ''
        self.ip_address = ''
        self.current_flows = None
        self.current_results = []

    def setup_compaign(self, flows):
        # check traffic generation requirements
        result_check = Sender.check_requirements()
        if not result_check:
            return result_check
        self.current_flows = flows
        return True

    def basic_ping(self):
        print 'sender working'  # test purpose only

    @staticmethod
    def get_command_itg_send(flow):
        s = "-a " + flow.destination + " -T " + flow.protocol + " -t " + \
            str(flow.trans_duration * 1000) + " " + flow.idt_distro + " "
        for i in flow.idt:
            s += str(i) + " "
        s += flow.ps_distro + " "
        for i in flow.idt:
            s += str(i) + " "
        s.strip()
        return s

    def start_compaign(self):
        try:
            f = open("script", "a+")
            for flow in self.current_flows:
                f.write(Sender.get_command_itg_send(flow))
                f.write('\n')
            f.close()
            command = ["ITGSend", "script", "-x", "logfile" + str(self.ip_address)]
            out = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = out.communicate()
            os.remove("script")
            for flow in self.current_flows:
                r = Pyro4.Proxy('PYRO:' + flow.destination + '_receiver@' + flow.destination + ':45000')
                result = r.get_result(flow)
                self.current_results.append(result)
            return self.current_results
        except Exception as e:
            print "start_compaign: ", str(e)

    @staticmethod
    def check_requirements():
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

