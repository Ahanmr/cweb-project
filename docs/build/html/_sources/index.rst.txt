Cluster Web Documentation
*************************

.. note:: ClusterWeb is currently in Beta, only the PBS API is available

Cluster Web is a Python library for creating wireless clusters of any devices that use SSH. This allows users to send jobs across a network of different kinds of devices. An example is a system that is made up of a laptop, CPU cluster, and a GPU workstation. Different jobs can be sent to each device all from the laptop and the results sent back to the laptop asynchronously.

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
- dill 
- pickle
- cloudpickle (host machine)


Basic Usage:
------------

.. code-block:: python

   from cweb.pbs import qsub
   import time

   def job(arg):
      a,b = 1,1
      for _ in range(int(arg)):
         a,b = b,a+b
      return a 

   def main():
       q = qsub.Qsub(job,1e5)
       q.connect('192.168.1.42')
       q.push()
       q.pull()

       while not q.complete:
           time.sleep(1)

       print(q.result)

   if __name__ == "__main__":
      main()

See more examples: :ref:`Beginner Usage Tutorials`

CWeb Documentation
******************

.. toctree::
   :maxdepth: 6
   :caption: About ClusterWeb

   why

   about

   install

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
