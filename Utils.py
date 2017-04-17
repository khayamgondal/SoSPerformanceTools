class StatsList(object):
  def __init__(self, hostname, cpu):
    self.hostname = hostname
    self.cpu = cpu
    
class SwitchStatList(object):
  def __init__(self, switch_id, rx_bits, tx_bits):
    self.switch_id = switch_id
    self.rx_bits = rx_bits
    tx_bits = tx_bits