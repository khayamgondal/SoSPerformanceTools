import httplib
import json
from RestCore import RestCore

class SwitchBandwidthStats(RestCore):
  
    def __init__(self, server, port):
        super(SwitchBandwidthStats, self).__init__(server, port)
	#self.dpid = dpid
	#self.s_port = s_port

    def get(self, data, dpid, s_port):
        ret = self.rest_call({}, dpid, s_port, 'GET')
        return json.loads(ret[2])

    def rest_call(self, data, dpid, s_port, action):
        path = 'wm/statistics/bandwidth/'+dpid+'/'+s_port+'/json' #next use %
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
  
