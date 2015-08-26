testing phone networks with GSM modules


### requirements
* one or more eno hardware nodes (Beaglebone Black + a Fona module)
* Python 2.7


### installation

```shell
$ pip install eno
```


### usage
A cluster of eno hardware nodes are setup
with network connectivity to a testing machine.
The testing machine uses `eno.nodes.Node` to control the connected nodes
and to read data from them.
The nodes themselves run the `eno.server.app`.
Other clients (like the testing machine) connect to this server
to give instructions to the hardware and to read data back.
The hardware uses [python-gsmmodem](https://github.com/faucamp/python-gsmmodem)
to communicate with the onboard GSM modem.

The testing machine should have an `~/.enorc` describing the test cluster:

```yaml
- name: node A
  ip_address: 192.168.1.102
  sim: endaga
- name: node B
  ip_address: 192.168.1.105
  sim: endaga
- name: node C
  ip_address: 192.168.1.107
  sim: ting
  phone_number: 19195551234
```

See additional examples in `server.py` and `sample_test.py`.


### license
MIT


### releases
* 0.0.2 - adds SMS handling capabilities
* 0.0.1 - barebones setup for pypi


### release process
you need a `~/.pypirc` like this:

```
[distutils]
index-servers =
  pypi

[pypi]
repository: https://pypi.python.org/pypi
username: yosemitebandit
password: mhm
```

bump the versions in `setup.py` and here in the readme, then run:

```shell
$ git tag 0.0.1 -m 'eno-python v0.0.1'
$ git push origin master --tags
$ python setup.py sdist upload -r pypi
```
