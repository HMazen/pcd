def enum(**enums):
    return type('Enum', (), enums)


Metrics = enum(jitter='jitter', packet_loss='packet loss', bit_rate='bit rate', delay='delay')

Protocols = enum(tcp='TCP', udp='UDP')

Ps_distro = enum(constant='-c', uniform='-u', exponential='-e', normal='-n',
                 poisson='-o', pareto='-v', cauchy='-y', gamma='-g', weibull='-w')
Idt_disto = enum(constant='-C', uniform='-U', exponential='-E', normal='-N',
                 poisson='-O', pareto='-V', cauchy='-Y', gamma='-G', weibull='-W')



class flow_config(object):
    ''' This  class holds the definition
    of a flow between a pair of points'''

    def __init__(self):
        self.flow_id = 123456
        self.source = '127.0.0.1'  # source node address
        self.destination = '127.0.0.1'  # destination node address
        self.protocol = 'TCP'  # protocol type
        self.ps = []  # packet size in bytes
        self.ps_distro = ''  # packet size distribution
        self.idt = []  # inter departure time
        self.idt_distro = ''  # inter departure time distribution
        self.starting_date = 0  # transmission start date
        self.trans_duration = 5  # transmission duration
        self.mesure = None


class compaign_config(object):
    ''' Holds the list of flows defining the compaign '''
    def __init__(self, flows):
        self.flows = flows
        self.is_multicast = False

    def add_flow(self, flow):
        self.flows.append(flow)

    def get_senders(self):
        s = []
        for flow in self.flows:
            if not s.count(flow.source):
                s.append(flow.source)
        return s

    def get_receivers(self):
        r = []
        for flow in self.flows:
            if not r.count(flow.destination):
                r.append(flow.destination)
        return r

    def get_flows_by_sender(self, sender):
        return [flow for flow in self.flows if flow.source == sender]


class mesure_config(object):
    ''' Definition of a mesure configuration '''
    def __init__(self):
        self.metrics = []  # list of metrics
        self.start_date = ''  # estimated starting date
        self.finish_date = ''  # estimated finish date
        self.sampling_interval = 5  # sampling interval in seconds


class metric(object):
    ''' Definition of a metric, eg: bandwidth, jitter... '''
    def __init__(self, name=''):
        self.name = name  # metric name
        self.values = {}


class result(object):
    def __init__(self):
        self.metrics = []
        self.flow_id = None
