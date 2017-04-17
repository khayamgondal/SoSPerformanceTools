#This file will do an SSH to requested node and will return the results.
#Make sure that user and authentication method is defined in start_app.py file.
#AUTHOR KANJAM
import subprocess

def run_command(user, node, command):
  ssh = subprocess.Popen(["ssh", user+"@"+node, command],
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
  result = ssh.stdout.readlines()
  if result == []:
    error = ssh.stderr.readlines()
    return -1, error
  else:
    return 0, result
    
def get_cpu_usage(literal):
  try:
    parts = literal[0].split() # 8th part is actual CPU usage
    return parts[8]
  except IndexError:
    return 0
def get_net_usage(literals):
  return literals[0].strip()
   
  #recv = list()
  #send = list()
  #for literal in literals:
  #  parts = literal.split() #split the string based
  #  recv.append(int (parts[1]))
  #  send.append(int (parts[2]))
  #return sum(recv), sum(send)
  
def get_hostname(literal):
  return literal[0].split('.')[0]
