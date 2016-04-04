class flow_config(object):
	''' This  class holds the definition
	of a flow between a pair of points'''

	def __init__(self):
		self.flow_id = 123456
		self.source = '192.168.1.5'	# source node address
		self.destination = '192.168.1.5'		# destination node address
		self.protocol = 'tcp'		# protocol type
		self.ps = 1500				# packet size in bytes
		self.ps_distro = ''			# packet size distribution
		self.idt = 0				# inter departure time
		self.idt_distro = ''		# inter departure time distribution
		self.starting_date = 0		# transmission start date
		self.trans_duration = 60	# transmission duration
		self.mesure = None


class compaign_config(object):
	''' Holds the list of flows defining the compaign '''
	def __init__(self, flows = []):
		self.flows = flows

	def add_flow(self, flow):
		self.flows.append(flow)

	def get_senders(self):
		s = []
		for flow in self.flows:
			s.append(flow.source)
		return s

	def get_receivers(self):
		r = []
		for flow in self.flows:
			r.append(flow.destination)
		return r


class mesure_config(object):
	''' Definition of a mesure configuration '''
	def __init__(slef):
		self.metrics = []				# list of metrics
		self.start_date = ''			# estimated starting date
		self.finish_date = ''			# estimated finish date
		self.sampling_interval = 5		# sampling interval in seconds


class metric(object):
	''' Definition of a metric, eg: bandwidth, jitter... '''
	def __init__(self, name='', flow_id='', min=0, max=100, average=50):
		self.flow_id = ''				# flow id 
		self.name = name				# metric name
		self.min = min					# min value mesured
		self.max = max					# max value mesured
		self.average = average			# verage value mesured

class result(object):
	def __init__(self):
		self.metrics = []
		self.flow_id = None
