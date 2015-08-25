"""Sample eno tests.

These would run on a technician's laptop but make HTTP calls out to various eno
nodes.
"""

import random
import unittest

import eno


class SampleTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    """Init each node."""
    # This verifies each node is on and reachable.  This will read data from
    # the ~/.enorc on this machine.
    cls.node_one = eno.get_node('node one')
    cls.node_two = eno.get_node('node two')
    cls.node_three = eno.get_node('node three')
    cls.node_four = eno.get_node('node four')
    cls.nodes = [cls.node_one, cls.node_two, cls.node_three, cls.node_four]
    # Make sure each node has a phone number (one may already be specified in
    # the .enorc file).  If a node doesn't have a number, do any necessary
    # registration here.
    for node in cls.nodes:
      if not node.phone_number:
        # Register the SIM..
        pass

  @classmethod
  def tearDownClass(cls):
    # Deregister each node as necessary.
    pass

  def setUp(self):
    """Reset the logs on each node."""
    for node in self.nodes:
      node.reset_log('sms')
      node.reset_log('call')
      node.reset_log('data')

  def test_sms(self):
    """We can send messages between nodes."""
    message = 'have some secret data: %s' % random.randint(0, 1e6)
    self.node_one.sms(self.node_two.phone_number, message)
    # Block until that specific message is received.
    self.assertTrue(self.node_two.wait_for_activity('sms', text=message))

  def test_call(self):
    """We can make a call from one node to another."""
    self.node_one.call(self.node_two.phone_number)
    # Block until a call is received from that number.
    self.assertTrue(
      self.node_two.wait_for_activity(
        'call', sender=self.node_one.phone_number))

  def test_data_access(self):
    """We can use data services."""
    target = 'http://google.com'
    self.node_one.data(target)
    self.node_one.wait_for_activity('data', target=target)
    data_log = self.node_one.get_log('data')
    self.assertTrue(target in data_log)
    self.assertTrue(data_log[target]['bytes_received'] > 0)

  def test_two_concurrent_calls(self):
    """We can support two simultaneous calls."""
    self.node_one.call(self.node_two.phone_number, hangup_immediately=False)
    self.node_three.call(self.node_four.phone_number, hangup_immediately=False)
    # Check that we have two calls going.
    self.assertTrue(
      self.node_two.wait_for_activity(
        'call', sender=self.node_one.phone_number))
    self.assertTrue(
      self.node_four.wait_for_activity(
        'call', sender=self.node_three.phone_number))
    # End both calls.
    self.node_one.hangup()
    self.node_three.hangup()
