#!/usr/bin/python
import ConfigParser as cp
#import spur
import time
from SshHelper.SshHelper import run_command, get_cpu_usage, get_net_usage, get_hostname
from ControllerStats.SwitchStats import SwitchStats

# Read the agents/servers/clients list from config file
config_file = "config"
parser = cp.ConfigParser()
parser.read(config_file)
user = parser.get('NODES', 'user')
nodes = parser.get('NODES', 'nodes').split(',')
passwd = parser.get('NODES', 'pass')
key = parser.get('NODES', 'key')
nic = parser.get('NODES', 'nic')

controller_ip = parser.get('CONTROLLER', 'ip')
controller_port = parser.get('CONTROLLER', 'port')

switchStats = SwitchStats(controller_ip, controller_port)
print (switchStats.get(None))

#Get the switch stats
# Now we will do SSH into each node and get the stats. 
while (1):
  print time.time()
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

