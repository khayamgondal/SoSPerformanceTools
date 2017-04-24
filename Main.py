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
      
    file_handler = open('/var/www/html/sos/'+hostname+'_net', 'a+')
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
      if send < 0.005:
        send = 0
      if recv < 0.005:
        recv = 0
    print hostname+'_net', recv, send
    file_handler.write(str(strftime("%H:%M:%S", )) + ',' + str(recv) +','+ str(send) + '\n')
    file_handler.close();

def worker_con():

  switchStats = SwitchStats(controller_ip, controller_port).get(None)
  switchBandwidthStats = SwitchBandwidthStats(controller_ip, controller_port)
  while(1):
    totalBW = 0
    for i in xrange(len(switchStats)): #Itterate over each switch
      switch_bw = switchBandwidthStats.get(None, switchStats[i]['switchDPID'], '0')
      if switch_bw: 
        for sw in switch_bw:
          if str(sw['dpid']).startswith('00:00'): # its a virtual switch 
            if sw['port'] == 'local':
              file_handler = open('/var/www/html/sos/'+str(sw['dpid']).translate(None, ':!@#$'), 'a+')
              tx = float(sw['bits-per-second-tx'])/1000000000
              rx = float(sw['bits-per-second-rx'])/1000000000
              if tx < 0.05:
                tx = 0
              if rx < 0.05:
                rx = 0
              print 'Virtual Switches' , tx, rx
              totalBW += tx
              file_handler.write(str(strftime("%H:%M:%S", )) + ',' + str(tx) +','+ str(rx) + '\n')
          #elif str(sw['dpid']).startswith('00:02:00:01:e8:a7:a7:15'): 
            #if sw['port'] == '21':
              #file_handler = open('/var/www/html/sos/controller', 'a+')
              #tx = float(sw['bits-per-second-tx'])/1000000000
              #rx = float(sw['bits-per-second-rx'])/1000000000
              #print 'Phsyical', tx, rx
              #file_handler.write(str(strftime("%H:%M:%S", )) + ',' + str(tx) +','+ str(rx) + '\n')
              #file_handler.close();
      file_handler = open('/var/www/html/sos/controller', 'a+')
      file_handler.write(str(strftime("%H:%M:%S", )) + ',' + str(totalBW/2) +','+ str(totalBW/2) + '\n')
      file_handler.close();
      print 'Total BW ' + str(totalBW/2)
    time.sleep(0.5)

    #switch_bw = switchBandwidthStats.get(None, '00:02:00:01:e8:a7:a7:15', '21')
    #for sw in switch_bw:

        
#MULTITHREADING SUPPORT
threads = []
for node in nodes:
  status, hostname = run_command(user, node, "hostname")
  hostname = get_hostname(hostname)
  t = threading.Thread(target=worker_cpu, args=(node, hostname))  
  t2 = threading.Thread(target=worker_network, args=(node, hostname)) 
  t3 = threading.Thread(target=worker_con, ) 
  t.daemon = True
  t2.daemon = True
  t3.daemon = True
  
  threads.append(t)
  threads.append(t2)
  threads.append(t3)
  
  t.start()
  #t2.start()
  t3.start()

      
while(1):
  #Get the controller stats
  time.sleep(1)