#!/usr/bin/python
import ConfigParser as cp
import time
import json
from SshHelper.SshHelper import run_command, get_cpu_usage, get_net_usage, get_hostname
from ControllerStats.SwitchStats import SwitchStats
from ControllerStats.SwitchBandwidthStats import SwitchBandwidthStats

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


#Get the controller stats
switchStats = SwitchStats(controller_ip, controller_port).get(None)
switchBandwidthStats = SwitchBandwidthStats(controller_ip, controller_port)

for i in xrange(len(switchStats)):
  switch_bw = switchBandwidthStats.get(None, switchStats[i]['switchDPID'], '1')
  print (switch_bw[0]['bits-per-second-rx'])
  print (switch_bw[0]['bits-per-second-tx'])

# Now we will do SSH into each node and get the stats. 
while (1):
  print time.time()
  for node in nodes:
    status, hostname = run_command(user, node, "hostname")
    status, cpu = run_command(user, node, "top -bn 1 | grep agent")
    #status, network = run_command(user, node, "netstat -tnp | grep agent")
    #status, network_recv = run_command(user, node, "cat /sys/class/net/" +nic+
    #"/statistics/rx_bytes")
    #status, network_send = run_command(user, node, "cat /sys/class/net/" +nic+
    #"/statistics/tx_bytes")
  
    cpu = get_cpu_usage(cpu)
    #recv = get_net_usage(network_recv)
    #send = get_net_usage(network_send)
    hostname = get_hostname(hostname)
    print hostname, cpu

