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
				if not sender.check_requirments():
					unreach_senders.append(sender)
				# get remote sender
			except e:
				unreach_senders.append(sender)

		for recv in receivers:
			try:
				result_check = recv.check_requirments()
				print result_check
				if not result_check:
                                        unreach_receivers.append(recv)
				elif result_check == 'server is already running':
					print result_check
				# get remote sender
			except e:
				unreach_receivers.append(recv)
		# process check results
		#TODO : traiter le cas ou il y a des senders ou receivers inaccessibe
		
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
	master = Master()
	s = Pyro4.Proxy('PYRONAME:192.168.1.5_sender')
	r = Pyro4.Proxy('PYRONAME:192.168.1.5_receiver')
	master.check_hosts_availability([s], [r])

