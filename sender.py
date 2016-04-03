import Pyro4
from subprocess import *

class Sender(object):

	def __init__(self):
		self.results = []
		self.master_ip = ''
		self.remote_receiver = None
		self.remote_master = None
		self.num_flows = 0

	def setup_compaign(self, flow_config, master_ip):
		''' invoked by master to setup the compaign'''

		# setup the communication with the master
		if not self.master_ip:
			self.master_ip = master_ip
		if not self.remote_master:
			try:
				self.remote_master = get_remote_master()
			except e:
				pass
				# TODO: hansle exception

		# check traffic generation requirments
		test = check_requirments()
		if not test:
			pass
			# TODO: handle failure test
		
		# setup communication with receiver
		if not self.remote_receiver:
			try:
				self.remote_receiver = get_remote_receiver()
			except e:
				pass
				# TODO: handle exception

		status = ''
		try:
			status = self.remote_receiver.setup_rcv(flow_config.source)
		except e:
			pass
				# TODO: handle exception

		return status


	def basic_ping(self):
		print 'sender working'		# test purpose only


	def post_result(self, result):
		''' for the receiver to post results '''
		results.append(result)

	def start_compaign(self):
		pass

	def check_requirments(self):
		try:
			command=["iperf3","-v"]
			out = Popen(command, stdout = PIPE,stderr= PIPE)
			(stdout,stderr) = out.communicate()
			
			command=["ITGSend","-h"]
                        out = Popen(command, stdout = PIPE,stderr= PIPE)
                        (stdout,stderr) = out.communicate()
			return True
		except:
			return False

