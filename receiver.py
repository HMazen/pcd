from subprocess import Popen , PIPE
import sys
import multiprocessing
import time
def job(command):
	try:
		out = Popen(command, stdout = PIPE,stderr= PIPE)
		(stdout,stderr) = out.communicate()
	except:
		sys.exit(3)



class Receiver(object):

	def __init__(self):
		self.sender_ip = ''
		self.remote_sender = None
		self.result = None
		self.proc = None

	def setup_rcv(self, source_ip):
		self.sender_ip = source_ip
		status = check_requirments()
		return status

	def basic_ping(self):
		print 'receiver working'	# test purpose only
	
	def check_requirments(self):
		try:
			command=["iperf3","-s"]
			if not self.proc:
				self.proc = multiprocessing.Process(target = job , args = (command,))
				self.proc.start()
				time.sleep(1)
				if self.proc.exitcode == None:
					return True
				else:
					return False
			else:
				return "server is already running"
		except Exception as e:
			return str(e)
	def terminate_proc(self):
		if self.proc:
			self.proc.terminate()
			ps = Popen(('ps', '-ef'), stdout=PIPE)
			output = check_output(('grep', '[i]perf3'), stdin=ps.stdout)
			ps.wait()
			server_pid = output.split()[1]
			if server_pid: 
				Popen(('kill', server_pid), stdout=PIPE)
				ps.wait()
			self.proc = None
