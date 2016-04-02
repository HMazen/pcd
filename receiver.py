import Pyro4
#modified
class Receiver(object):

	def __init__(self):
		self.sender_ip = ''
		self.remote_sender = None
		self.result = None


	def setup_rcv(self, source_ip):
		self.sender_ip = source_ip
		status = check_requirments()
		return status

	def check_requirments(self):
		pass

	def basic_ping(self):
		print 'receiver working'	# test purpose only

