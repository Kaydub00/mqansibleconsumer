import stomp
from stomp import ConnectionListener
import json
from pyansible import *


queuename = "QUEUE_NAME_HERE"


class AnsibleConsumer(ConnectionListener):
  def on_error(self, headers, message):
    print "error"

  def on_message(self, headers, message):
    data = json.loads(message)
    print "received message"



if __name__ == "__main__":
  conn = stomp.Connection([('localhost',61613)])
  conn.set_listener('',AnsibleConsumer())
  conn.start()
  conn.connect()
  conn.subscribe(destination=queuename,id=1,ack='auto',headers={'transformation' : 'jms-map-json'})
  time.sleep(28800)
  conn.disconnect()
