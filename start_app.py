#!/usr/bin/python
#AUTHOR KANJAM

import ConfigParser as cp
#import spur
from ssh_commands import run_command, get_cpu_usage, get_net_usage, get_hostname
# Read the agents/servers/clients list from config file
config_file = "config"
parser = cp.ConfigParser()
parser.read(config_file)
user = parser.get('NODES', 'user')
nodes = parser.get('NODES', 'nodes').split(',')
passwd = parser.get('NODES', 'pass')
key = parser.get('NODES', 'key')
nic = parser.get('NODES', 'nic')

# Now we will do SSH into each node and get the stats. 
for node in nodes:
  status, hostname = run_command(user, node, "hostname")
  status, cpu = run_command(user, node, "top -bn 1 | grep agent")
  #status, network = run_command(user, node, "netstat -tnp | grep agent")
  status, network_recv = run_command(user, node, "cat /sys/class/net/" +nic+
  "/statistics/rx_bytes")
  status, network_send = run_command(user, node, "cat /sys/class/net/" +nic+
  "/statistics/tx_bytes")

  cpu = get_cpu_usage(cpu)
  recv = get_net_usage(network_recv)
  send = get_net_usage(network_send)
  hostname = get_hostname(hostname)
  print hostname, cpu, recv, send









#shell = spur.SshShell(
#    hostname=nodes[0],
#    username=user,
#    private_key_file = key,
     #password=passwd,
     #missing_host_key=spur.ssh.MissingHostKey.accept

#)
#result = shell.run(["top", "-bn 1 | grep agent"])
#print(result.output) # prints hello
#ssh = subprocess.Popen(["ssh", "%s" % nodes[0], 'top -bn 1 | grep agent'],
#                       shell=False,
#                       stdout=subprocess.PIPE,
#                       stderr=subprocess.PIPE)
#result = ssh.stdout.readlines()
#if result == []:
#    error = ssh.stderr.readlines()
#    print >>sys.stderr, "ERROR: %s" % error
#else:
#    print result
   
#ssh = paramiko.SSHClient()
#key = paramiko.RSAKey.from_private_key_file(".ssh/id_rsa")
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#try:
#  ssh.connect(nodes[0], username=user, password = passwd )
#ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls")
#  stdin, stdout, stderr = ssh.exec_command('uname -a')
#  print "output: ", stdout.read()
#  ssh.close()
  
#except paramiko.SSHException, e:
#  type, value, traceback = sys.exc_info()  
#  print('Error opening %s: %s' % (value, sys.exc_info()))

#except paramiko.AuthenticationException, e:
#  print  e
#except socket.error, e:
#  print "Socket connection failed:", e