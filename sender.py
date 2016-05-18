#!/usr/bin/python
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
        self.is_multicast = False
        self.multicast_address = ''

    def setup_compaign(self, flows, is_multicast):
        # check traffic generation requirements
        result_check = Sender.check_requirements()
        if not result_check:
            return result_check
        self.is_multicast = is_multicast
        self.current_flows = flows
        return True

    @staticmethod
    def get_command_itg_send(flow):
        s = "-a " + flow.destination + " -T " + flow.protocol + " -t " + \
            str(flow.trans_duration * 1000) + " " + flow.idt_distro + " "
        for i in flow.idt:
            s += str(i) + " "
        s += flow.ps_distro + " "
        for i in flow.ps:
            s += str(i) + " "
        s.strip()
        print s
        return s

    def start_compaign_unicast(self):
        try:
            f = open("script", "a+")
            for flow in self.current_flows:
                f.write(Sender.get_command_itg_send(flow))
                f.write('\n')
            f.close()
            command = ["ITGSend", "script", "-x", "logfile" + str(self.ip_address)]
            p = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = p.communicate()

            os.remove("script")
            for flow in self.current_flows:
                r = Pyro4.Proxy('PYRO:' + flow.destination + '_receiver@' + flow.destination + ':45000')
                result = r.get_result_unicast(flow)
                self.current_results.append(result)
            return self.current_results

        except Exception as e:
            print "start_compaign: ", str(e)

    def start_compaign_multicast(self):
        try:
            if len(self.current_flows) != 1:
                return "only one flow is allowed in multicast mode"
            command = ["iperf", "-c", self.multicast_address, "-u", "-t",
                       str(self.current_flows[0].trans_duration)]
            p = Popen(command, stdout=PIPE, stderr=PIPE)
            p.communicate()

            for flow in self.current_flows:
                r = Pyro4.Proxy('PYRO:' + flow.destination + '_receiver@' + flow.destination + ':45000')
                result = r.get_result_multicast(flow)
                print result
                self.current_results.append(result)
            return self.current_results
        except Exception as e:
            print "start_compaign multicast: ", str(e)

    def start_compaign(self):
        try:
            del self.current_results[:]
            if not self.is_multicast:
                return self.start_compaign_unicast()
            else:
                return self.start_compaign_multicast()
        except Exception as e:
            print "sender: start_compign ", str(e)

    @staticmethod
    def check_requirements():
        try:
            command = ["iperf", "-v"]
            out = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = out.communicate()
            command = ["ITGSend", "-h"]
            out = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = out.communicate()
            return True
        except:
            return False

