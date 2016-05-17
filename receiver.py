import multiprocessing
import os
import re
import sys
import time
from subprocess import Popen, PIPE, check_output

from serialization import *


def job(command):
    try:
        with open("re", "w+") as out:
            p = Popen(command, stdout=out, stderr=PIPE)
            p.communicate()
    except Exception as e:
        print "receiver job: ", str(e)
        sys.exit(3)


class Receiver(object):
    def __init__(self):
        self.ip_address = ''
        self.multicast_address = ''
        self.sender_ip = ''
        self.remote_sender = None
        self.result = None
        self.proc = None

    def basic_ping(self):
        print 'receiver working'  # test purpose only

    def check_requirments(self, is_multicast):
        self.terminate_proc()
        try:
            if is_multicast:
                command = ["iperf", "-s", "-B", self.multicast_address, "-u", "-i", "1"]
            else:
                command = ["ITGRecv", "-a", self.ip_address]
            if not self.proc:
                self.proc = multiprocessing.Process(target=job, args=(command,))
                self.proc.start()
                time.sleep(1)
                if self.proc.exitcode == None:
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            print "receiver check_requirments ", str(e)

    def terminate_proc(self):
        try:
            if self.proc:
                self.proc.terminate()
                self.proc = None
        except:
            pass
        try:
            ps = Popen(('ps', '-ef'), stdout=PIPE)
            output = check_output(('grep', '[I]TGRecv'), stdin=ps.stdout)
            ps.wait()
            server_pid = output.split()[1]
            if server_pid:
                Popen(('kill', server_pid), stdout=PIPE)
                ps.wait()
        except:
            try:
                ps = Popen(('ps', '-ef'), stdout=PIPE)
                output = check_output(('grep', '[i]perf'), stdin=ps.stdout)
                ps.wait()
                server_pid = output.split()[1]
                if server_pid:
                    Popen(('kill', server_pid), stdout=PIPE)
                    ps.wait()
            except:
                pass

    def get_result_unicast(self, flow):
        try:
            mesure = flow.mesure
            ps = Popen(['ITGDec', 'logfile' + str(flow.source), '-c', str(mesure.sampling_interval),
                        'result' + str(flow.flow_id)], stdout=PIPE).communicate()
            bitrate = metric()
            bitrate.name = Metrics.bit_rate
            delay = metric()
            delay.name = Metrics.delay
            jitter = metric()
            jitter.name = Metrics.jitter
            packet_loss = metric()
            packet_loss.name = Metrics.packet_loss
            with open("result" + str(flow.flow_id)) as f:
                for s in f.readlines():
                    metrics = s.split()
                    bitrate.values[float(metrics[0])] = float(metrics[1])
                    delay.values[float(metrics[0])] = float(metrics[2])
                    jitter.values[float(metrics[0])] = float(metrics[3])
                    packet_loss.values[float(metrics[0])] = float(metrics[4])
            r = result()
            for m in mesure.metrics:
                if m == "jitter":
                    r.metrics.append(jitter)
                elif m == "packet loss":
                    r.metrics.append(packet_loss)
                elif m == "delay":
                    r.metrics.append(delay)
                else:
                    r.metrics.append(bitrate)

            r.flow_id = flow.flow_id
            try:
                os.remove("logfile" + str(flow.source))
            except:
                pass
            try:
                os.remove("result" + str(flow.flow_id))
            except:
                pass
            return r
        except Exception as e:
            print "receiver get_result: ", str(e)

    def get_result_multicast(self, flow):
        try:
            mesure = flow.mesure
            bitrate = metric()
            bitrate.name = Metrics.bit_rate
            delay = metric()
            delay.name = Metrics.delay
            jitter = metric()
            jitter.name = Metrics.jitter
            packet_loss = metric()
            packet_loss.name = Metrics.packet_loss
            with open("re", "r") as f:
                test = False
                for s in f.readlines():
                    if test:
                        metrics = re.split('\s+', s)
                        bitrate.values[float(metrics[3])] = float(metrics[5])
                        jitter.values[float(metrics[3])] = float(metrics[9])
                        packet_loss.values[float(metrics[3])] = (
                            float(metrics[11].replace('/', '')) / float(metrics[12]))
                        print packet_loss.values
                    if s.find("Transfer") != -1:
                        test = True
            r = result()
            for m in mesure.metrics:
                if m == "jitter":
                    r.metrics.append(jitter)
                elif m == "packet loss":
                    r.metrics.append(packet_loss)
                elif m == "delay":
                    r.metrics.append(delay)
                else:
                    r.metrics.append(bitrate)
            r.flow_id = flow.flow_id
            print "multicast with success"
            return r
        except Exception as e:
            print "receiver get_result: ", str(e)
