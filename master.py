import Pyro4
from utilities import *




class Master(object):

	def __init__(self):
		self.pending_compaigns = []
		self.pending_flow_results = []
		self.results = []
		self.current_senders = []
		self.current_receivers = []

	def post_compaign_config(self, config):
		if self.has_pending_compaigns(): return
		self.pending_compaigns.append(config)
		result_check = self.check_hosts_availability(config.get_senders(), config.get_receivers())
		if result_check == True:
			for sender in self.current_senders:
				result = sender.start_compaign()
			#TODO: céer un processus pour chaque sender
			#TODO: traiter l'erreur dans le cas de l'échec de start_compaign

	def check_hosts_availability(self, senders, receivers):
		''' Internal method to check hosts 
			for remote objects ''' 
		unreach_senders = []
		unreach_receivers = []
		
		for sender in senders:
			try:
				s = Pyro4.Proxy('PYRONAME:'+sender+'_sender')
				if not s.check_requirments():
					unreach_senders.append(sender)
				else:
					self.current_senders.append(s)
			except:
				unreach_senders.append(sender)

		for recv in receivers:
			try:
				r = Pyro4.Proxy('PYRONAME:'+recv+'_receiver')
				result_check = r.check_requirments()
				if not result_check:
                                        unreach_receivers.append(recv)
				elif result_check == 'server is already running':
					print result_check
					#TODO: traiter le cas de "server is running"
				else:
					self.current_receivers.append(r)
			except:
				unreach_receivers.append(recv)
		if not unreach_senders and not unreach_receivers:
			return True
		else:
			return False
		# process check results
		#TODO : traiter le cas ou il y a des senders ou receivers inaccessibe
		
	def has_pending_compaigns(self):
		return len(self.pending_compaigns)

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
	config = compaign_config([flow_config()])
	master.post_compaign_config(config)	

