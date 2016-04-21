from subprocess import *

import Pyro4


class Sender(object):
    def __init__(self):
        self.results = []
        self.master_ip = ''
        self.remote_receiver = None
        self.remote_master = None
        self.num_flows = 0
        self.current_flows = None
        self.current_mesures = None
        self.current_results = []


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

    def get_command_itg_send(self, flow):
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
                f.write(self.get_command_itg_send(flow))
                f.write('\n')
            f.close()
            command = ["ITGSend", "script", "-x", "logfile"]
            out = Popen(command, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = out.communicate()
            # os.remove("script")
            for flow in self.current_flows:
                r = Pyro4.Proxy('PYRO:' + flow.destination + '_receiver@' + flow.destination + ':45000')
                result = r.get_result(flow)
                self.current_results.append(result)
            return self.current_results
        except Exception as e:
            print "start_compaign: ", str(e)

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

