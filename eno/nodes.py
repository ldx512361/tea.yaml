"""Abstraction of a remote eno hardware node."""

import requests


class Node(object):
  """Representation of a remote eno hardware node.

  This class is used on the testing machine to control a remote eno node.  The
  hardware itself does not use this class, it instead uses the control server.
  """

  def __init__(self):
    self.ip_address = ''
    self.sim = ''
    self.phone_number = ''

  def sms(self, phone_number, message):
    """Send an SMS."""
    data = {
      'phone_number': phone_number,
      'message': message,
    }
    endpoint = '%s/sms' % self.ip_address
    response = requests.post(endpoint, data=data)
    if response.status_code != 200:
      raise ValueError

  def call(self, phone_number, **kwargs):
    """Make a call.

    Args:
      phone_number: the number to call

    Kwargs:
      hangup_immediately: whether to hangup immediately after the call is
                          answered (default is True)
    """
    hangup_immediately = kwargs.get('hangup_immediately', True)
    data = {
      'phone_number': phone_number,
      'hangup_immediately': hangup_immediately,
    }
    endpoint = '%s/call' % self.ip_address
    response = requests.post(endpoint, data=data)
    if response.status_code != 200:
      raise ValueError

  def hangup(self):
    """Terminates any ongoing call."""
    endpoint = '%s/hangup' % self.ip_address
    response = requests.post(endpoint)
    if response.status_code != 200:
      raise ValueError

  def data(self, target):
    """Use data services.

    Args:
      target: will send an HTTP GET to this address
    """
    data = {
      'target': target,
    }
    endpoint = '%s/data' % self.ip_address
    response = requests.post(endpoint, data=data)
    if response.status_code != 200:
      raise ValueError

  def wait_for_activity(self, activity, **kwargs):
    """Block until some activity completes.

    This could mean waiting until an SMS is received, waiting until a call is
    received or blocking until data is returned from a website.

    Args:
      activity: one of sms, call or data

    Kwargs:
      body: blocks until an SMS with this particular message is received
      sender: blocks until a call from this number is received
      target: blocks until data from this target is received
      timeout: the max amount of time to block (default: 10s)
    """

  def get_log(self, activity):
    """Gets info from an activity log.

    Args:
      activity: one of sms, call or data
    """
    if activity not in ('sms', 'call', 'data'):
      raise ValueError
    endpoint = '%s/log/%s' % (self.ip_address, activity)
    response = requests.get(endpoint)
    if response.status_code != 200:
      raise ValueError
    return response.json()

  def reset_log(self, activity):
    """Resets an activity log.

    Args:
      activity: one of sms, call or data
    """
    if activity not in ('sms', 'call', 'data'):
      raise ValueError
    endpoint = '%s/log/%s' % (self.ip_address, activity)
    response = requests.delete(endpoint)
    if response.status_code != 200:
      raise ValueError

def get_node(name):
  """Shortcut method to get an eno node's data.

  Args:
    name: the name of the node

  Returns a Node instance.
  """
