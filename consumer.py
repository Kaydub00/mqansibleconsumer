import stomp
from stomp import ConnectionListener
import json
from pyansible import *


queuename = "QUEUE_NAME_HERE"
playbook = "/location/of/playbook.yml"

class AnsibleConsumer(ConnectionListener):
  def on_error(self, headers, message):
    print "error"

  def on_message(self, headers, message):
    print "Message Received..."
    # get the data you need from your messages, this code is dependent on your data structures used
    data = json.loads(message)
    msg = data['list']['map']
    l = []
    if isinstance(msg, dict):
      msg = [msg]
    for item in msg:
      l.append(item['entry'])
    ib = InventoryBuilder(l)
    invfile = ib.getInventoryFile()
    pb = PlaybookRunner(invfile.name, playbook)
    results = pb.execute()
    os.remote(invfile.name)
    for host in l:
      result = results[host['hostname']]
      if result['unreachable'] > 0:
        # do something with unreachable hosts
        # for some workflows I just add them to a list and retry them, others I send them back to a different queue
        print "host is unreachable " + host['hostname']
      elif result['failures'] > 0:
        # do something for failures
        print "host has failures " + host['hostname']
      else:
        print "upgrades successful " + host['hostname']
    print "Waiting on next message..."

if __name__ == "__main__":
  conn = stomp.Connection([('localhost',61613)])
  conn.set_listener('',AnsibleConsumer())
  conn.start()
  conn.connect()
  # dont need this transformation if messages coming from a python app
  conn.subscribe(destination=queuename,id=1,ack='auto',headers={'transformation' : 'jms-map-json'})
  # Let's just run it for a few minutes
  time.sleep(600)
  conn.disconnect()
