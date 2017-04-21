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

def worker_cpu(node, hostname):
  while(1):
    file_handler = open('/var/www/html/sos/'+hostname, 'a+')
    status, cpu = run_command(user, node, "top -bn 1 | grep agent")
    cpu = get_cpu_usage(cpu)
    print hostname, cpu
    file_handler.write(str(strftime("%H:%M:%S", ))  + ',' + str(cpu) + '\n')
    file_handler.close();

def worker_network(node, hostname):
  last_recv = 0
  last_send = 0
  
  while(1):
    file_handler = open('/var/www/html/sos/plots'+hostname+'_net', 'a+')
    status, network_recv = run_command(user, node, "cat /sys/class/net/" +nic+
    "/statistics/rx_bytes")
    status, network_send = run_command(user, node, "cat /sys/class/net/" +nic+
    "/statistics/tx_bytes")
    
    recv = get_net_usage(network_recv)
    send = get_net_usage(network_send)
    
    if last_recv == 0:
      last_time = time.time()
      last_recv = recv
      last_send = send
      recv = 0
      send = 0
    else:
      recv = (float(recv) - float(last_recv)) / (float (time.time() ) - float(last_time) )
      recv = recv * 8 /1024 / 1024 / 1024
      send = (float(send) - float(last_send)) / (float (time.time() ) - float(last_time) )
      send = send * 8 /1024 / 1024 / 1024
      
    print hostname+'_net', recv, send
    file_handler.write(str(time.time()) + ',' + hostname + ',' + str(recv) +','+ str(send) + '\n')
    file_handler.close();


#MULTITHREADING SUPPORT
threads = []
for node in nodes:
  status, hostname = run_command(user, node, "hostname")
  hostname = get_hostname(hostname)
  t = threading.Thread(target=worker_cpu, args=(node, hostname))  
  t2 = threading.Thread(target=worker_network, args=(node, hostname)) 
  t.daemon = True
  t2.daemon = True
  threads.append(t)
  threads.append(t2)
  t.start()
  #t2.start()
  
while(1):
  time.sleep(1)