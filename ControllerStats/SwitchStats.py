import httplib
import json
from RestCore import RestCore

class SwitchStats(RestCore):

    def __init__(self, server, port):
        super(SwitchStats, self).__init__(server, port)
	
    def rest_call(self, data, action): #get the list of all the switches
        path = 'wm/core/controller/switches/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret
  
