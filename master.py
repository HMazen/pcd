import Pyro4

class Master(object):

	def __init__(self):
		self.pending_compaigns = []
		self.pending_flow_results = []
		self.results = []

	def post_compaign_config(self, config):
		if has_pending_compaings(): return
		self.pending_compaigns.append(config)
		check_hosts_availability(config.get_senders(), config.get_receivers())
		

	def check_hosts_availability(self, senders, receivers):
		''' Internal method to check hosts 
			for remote objects ''' 
		unreach_senders = []
		unreach_receivers = []
		
		for sender in senders:
			try:
				pass
				# get remote sender
			except e:
				unreach_senders.append(sender)

		for recv in receivers:
			try:
				pass
				# get remote sender
			except e:
				unreach_receivers.append(recv)

		# process check results
		
	def has_pending_compaings(self):
		return len(pending_compaigns)

	def post_result(self, result):
		''' A sender uses this method to deposit a result '''

		if result.flow_id in self.pending_flow_results:
			self.pending_flow_results.remove(result.flow_id)
			self.results.append(result)

	def basic_ping(self):
		return 'master working'		# test purpose only

	def call_sender(self, sender_ip):
		s = Pyro4.Proxy('PYRONAME:'+sender_ip+'_sender')
		s.basic_ping()
		

def main():
	master = Master()
#	config_file = open('file.cfg', 'r')
#	ip = config_file.read(15)
#	master_name = ip.strip() + '_master'

	Pyro4.Daemon.serveSimple(
			{ 
				master : 'master'
			},
			# host=ip,
			ns = True
		)


if __name__ == '__main__':
	main()
