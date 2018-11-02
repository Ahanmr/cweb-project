ClusterWeb Documentation
*************************

.. note:: ClusterWeb is currently in Beta, only the PBS API is available

.. sidebar:: Use Cases 

   - Connect to an existing cluster
   - Create a cluster with different devices
   - Test hardware and software configurations across many devices
   - Make custom distributed networks in Python
   - Run scripts all from a local machine across multiple clusters simultaneously

ClusterWeb is a Python library for creating compute clusters out of any devices that use SSH. 

Compatiable Devices
~~~~~~~~~~~~~~~~~~~
- CPUs nodes
- Desktops 
- GPUs workstations
- Laptops
- Raspberry Pi
- Android phones


Requirements
------------
- Python 3.6 or above
- SSH
- Linux or OSX
- pickle
- cloudpickle (host machine)


Basic Usage:
------------

.. code-block:: python

   from clusterweb.pbs.qsub import Qsub
   import time

   def job(arg):
      a,b = 0,1
      for _ in range(int(arg)):
         a,b = b,a+b
      return a 

   q = Qsub(job,1e5)
   q.push()
   q.pull(thread=False)

   print(q.result)

See more examples: :ref:`Beginner Usage Tutorials`

ClusterWeb Documentation
************************

.. toctree::
   :maxdepth: 6
   :caption: About ClusterWeb

   why

   about

   install

   getting_started

.. toctree::
   :maxdepth: 6
   :caption: Developer Resources

   beginner

   advanced

   cpu

.. toctree::
   :maxdepth: 6
   :caption: Portable Batch Systems (PBS)

   qsub

   qsession

   qdel

   qstat

   resources

.. toctree::
   :maxdepth: 6
   :caption: Secure Shell Systems (SSH)

   sub

   session

   del

   stat
