## This is just for Ansible 1.X, will need to be updated for Ansilbe 2
import jinja2
from tempfile import NamedTemporaryFile
from ansible import callbacks
from ansible import utils
import ansible.runner
import ansible.playbook

class InventoryBuilder:

  inventory = """[activegroup]
{% for item in locations -%}
{{ item }}
{% endfor %}
"""

  def __init__(self, hostlist):
    self.hostlist = hostlist

  def getInventory(self):
    inventory_template = jinja2.Template(self.inventory)
    rendered = inventory_template.render({'locations': self.hostlist})
    return rendered

  def getInventoryFile(self):
    hosts = NamedTemporaryFile(delete=False)
    hosts.write(self.getInventory())
    hosts.close
    return hosts


class PlaybookRunner:

  def __init__(self, inventoryfile, playbookfile):
    self.inventoryfile = inventoryfile
    self.playbookfile = playbookfile

  def execute(self):
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=1)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=1)
    pb = ansible.playbook.PlayBook(
      playbook=self.playbookfile,
      host_list=self.inventoryfile,
      stats=stats,
      callbacks=playbook_cb,
      runner_callbacks=runner_cb
    )
    ret = pb.run()
    return ret
