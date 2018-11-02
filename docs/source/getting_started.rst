Getting Started
===============

System Requirements
~~~~~~~~~~~~~~~~~~~

- Python 3.6 or above
- SSH
- Ubuntu or OSX

Python Requirements
~~~~~~~~~~~~~~~~~~~
- cloudpickle
- pickle


Setup SSH
#########

The library communicates with a remote cluster through Secure Shell Protocol (SSH). Since SSH does not work on Windows except through Putty, ClusterWeb does not currently support Windows.

Install SSH
-----------

If already installed, continue to the next section about creating the user ssh config file.

Ubuntu
++++++

SSH is not automatically installed and needs to be installed:

>>> sudo apt-get install openssh-server

Check to see if ssh has been installed correctly:

>>> sudo service ssh status

If you need to edit the ssh configuration file, it can be found with:

>>> sudo nano /etc/ssh/sshd_config

Save changes and reload SSH:

>>> sudo service ssh restart

OSX
+++

SSH is automatically included in modern OSX devices, check to see if it's installed correctly with:

>>> ssh
usage: ssh [-1246AaCfGgKkMNnqsTtVvXxYy] [-b bind_address] [-c cipher_spec]
           [-D [bind_address:]port] [-E log_file] [-e escape_char]
           [-F configfile] [-I pkcs11] [-i identity_file]
           [-J [user@]host[:port]] [-L address] [-l login_name] [-m mac_spec]
           [-O ctl_cmd] [-o option] [-p port] [-Q query_option] [-R address]
           [-S ctl_path] [-W host:port] [-w local_tun[:remote_tun]]
           [user@]hostname [command]

Setup the Default Address
#########################

Before using the PBS API for the first time, the default ssh address is 'localhost'. If the API will be used for only one cluster, change the default address to skip having to set the address every time.

.. code-block:: python
	
	from clusterweb.interfaces.ssh import SSH

	s = SSH()
	s.change_default('new_address')

This will check ~/.ssh/config for the address if it is not an ip address. To disable this check, pass False to the verify flag.

.. code-block:: python
	
	from clusterweb.interfaces.ssh import SSH

	s = SSH()
	s.change_default('new_address',verify=False)

Common Errors:
--------------

1. `SSH won't connect` This is an error with the SSH key and config settings, please check the config file and key file path.

