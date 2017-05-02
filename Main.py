#!/usr/bin/python
import ConfigParser as cp
import time
import json
from SshHelper.SshHelper import run_command, get_cpu_usage, get_net_usage, get_hostname
from ControllerStats.SwitchStats import SwitchStats
from ControllerStats.SwitchBandwidthStats import SwitchBandwidthStats
from Utils import StatsList, SwitchStatList
import signal, sys
import threading
from time import gmtime, strftime
from Workers import worker_cpu, worker_network, worker_con

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

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)

print "Writing outputs into files. Press Crtl + C to cancel "

        
#MULTITHREADING SUPPORT
threads = []
for node in nodes:
  status, hostname = run_command(user, node, "hostname")
  hostname = get_hostname(hostname)
  t = threading.Thread(target=worker_cpu, args=(user, node, hostname))  
  #t2 = threading.Thread(target=worker_network, args=(user, node, hostname)) 
  #t3 = threading.Thread(target=worker_con, args=(controller_ip, controller_port) ) 
  t.daemon = True
  #t2.daemon = True
  #t3.daemon = True
  
  threads.append(t)
  #threads.append(t2)
  #threads.append(t3)
  
  t.start()
  #t2.start()
  #t3.start()
  
t3 = threading.Thread(target=worker_con, args=(controller_ip, controller_port) )
t3.daemon = True
threads.append(t3)
#t3.start()
worker_con(controller_ip, controller_port)
      
while(1):
  #Get the controller stats

  time.sleep(1)