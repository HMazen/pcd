import Pyro4
from subprocess import *
from utilities import *

class Sender(object):

	def __init__(self):
		self.results = []
		self.master_ip = ''
		self.remote_receiver = None
		self.remote_master = None
		self.num_flows = 0
		self.current_compaign = None

	def setup_compaign(self, compaign, master_ip):
		''' invoked by master to setup the compaign'''

		# setup the communication with the master
		if not self.master_ip:
			self.master_ip = master_ip
		if not self.remote_master:
			try:
				#self.remote_master = self.get_remote_master()
			except e:
				pass
				# TODO: hansle exception

		# check traffic generation requirments
		result_check = self.check_requirments()
		if not result_check:
			return result_check

		self.current_compaign = compaign
		return True


	def basic_ping(self):
		print 'sender working'		# test purpose only


	def post_result(self, result):
		''' for the receiver to post results '''
		results.append(result)

	def start_compaign(self):
		flows = compaign.flows
		for flow in flows:
			#TODO: vérifier le fonctionnement de iperf et d-itg et écrire les flows dans un fichier 

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

