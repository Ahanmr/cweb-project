Beginner Usage Tutorials
========================

Submitting a Single Job with Qsub
---------------------------------

Send a job to the cluster that computes the millionth fibonacci
number. Similar to git, the main commands for sending and 
recieving data is push and pull. The pull command automatically
starts a thread in the background that checks for the result file
unless a negative thread arguement is passed to pull.

To run within the main thread:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from clusterweb.pbs import qsub
   import time

   def job(arg):
      a,b = 0,1
      for _ in range(int(arg)):
         a,b = b,a+b
      return a 

   def main():
       q = qsub.Qsub(job,1e6)
       q.push()
       q.pull(thread=False)
       print(q.result)

   if __name__ == "__main__":
      main()

To run asynchronous with the main thread:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from clusterweb.pbs import qsub
   import time

   def job(arg):
      a,b = 0,1
      for _ in range(int(arg)):
         a,b = b,a+b
      return a 

   def main():
       q = qsub.Qsub(job,1e6)
       q.push()
       q.pull()

       while not q.complete:
           time.sleep(1)

       print(q.result)

   if __name__ == "__main__":
      main()


Running Multiple Jobs on Multiple Nodes
---------------------------------------

.. code-block:: python

    from clusterweb.pbs import qsub
    import time

    def job(arg):
        a,b = 0,1
        for _ in range(int(arg)):
            a,b = b,a+b
        return a 

    def main():
        q1 = qsub.Qsub(job,5)
        q2 = qsub.Qsub(job,6)
        q3 = qsub.Qsub(job,7)

        q1.push()
        q2.push()
        q3.push()

        q1.pull()
        q2.pull()
        q3.pull()

        while not (q1.complete and q2.complete and q3.complete):
            time.sleep(1)

        print("The 5th fibonnaci number is: {}".format(q1.result))
        print("The 6th fibonnaci number is: {}".format(q2.result))
        print("The 7th fibonnaci number is: {}".format(q3.result))

    if __name__ == "__main__":
        main()

Compare with Local Machine
--------------------------

Use the cluster to compute the nth fibonacci number but also compare with the time required to compute with the local device. Increase or decrease `TEST_CONSTANT` to see at which threshold is it more efficient to use the cluster instead of the local machine. This is a way of testing how fast the connection to the cluster is and what kinds of functions are better to keep local.

.. code-block:: python

    import time

    from clusterweb.pbs.qsub import Qsub


    TEST_CONSTANT = int(1e6)

    def test(n):
        a,b=1,1
        for _ in range(n):
            a,b = b,a+b 
        return a


    def main():
        start_time = time.time()

        q = Qsub(test,TEST_CONSTANT)

        q.push()

        q.pull()

        while not q.complete:
            time.sleep(1)

        print(q.result)

        print("The cluster took {}s to complete with: {}".format(
            time.time()-start_time,TEST_CONSTANT))

        start_time = time.time()

        test(TEST_CONSTANT)

        print("The local machine took {}s to complete with: {}".format(
            time.time()-start_time,TEST_CONSTANT))

        
    if __name__ == "__main__":
        main()

Resource Allocation
-------------------

Sometimes scripts require more or less resources than the default configuration. This exercise will show how to adjust the amount of resources requested by the auto-generated PBS script. Note that these values go through error handling and will raise exceptions if they are invalid arguments. See the documentation for the rules regarding resource allocation.

.. code-block:: python

    import time

    from clusterweb.pbs.qsub import Qsub


    TEST_CONSTANT = int(1e3)

    def test(n):
        a,b=1,1
        for _ in range(n):
            a,b = b,a+b 
        return a


    def main():
        q = Qsub(test,TEST_CONSTANT)

        q.allocate_memory('16GB')

        q.allocate_nodes(2)

        q.push()

        q.pull()

        while not q.complete:
            time.sleep(1e-2)

        print(q.result)
 
    if __name__ == "__main__":
        main()

Using QSession to Run Multiple Jobs On One Node
-----------------------------------------------

.. code-block:: python

    from clusterweb.pbs.qsession import QSession
    import time

    def job(arg):
        a,b = 0,1
        for _ in range(arg):
            a,b = b,a+b
        return a 

    def main():

        sess = QSession()

        sess.load(job,1)
        sess.load(job,2)
        sess.load(job,3)
        sess.load(job,4)
        sess.load(job,5)

        sess.push()
        sess.pull()

        while not sess.all_complete:
            time.sleep(1)
            print("Waiting...\t{}".format(sess.results))

        print(sess.results)

    if __name__ == "__main__":
        main()

Using * to Create a QSession from Qsub Jobs
-------------------------------------------

.. code-block:: python

    from clusterweb.pbs import qsub
    import time

    def job(arg):
        a,b = 0,1
        for _ in range(arg):
            a,b = b,a+b
        return a 

    def main():
        q = qsub.Qsub(job,5)

        sess = q * 5

        sess.push()
        sess.pull()

        while not sess.all_complete:
            time.sleep(1)
            print("Waiting...")

        print(sess.results)

    if __name__ == "__main__":
        main()


Deleting a Job While Running With a Timer
-----------------------------------------

.. code-block:: python

    from clusterweb.pbs import qsub
    from clusterweb.pbs import qstat

    import time

    def job(arg):
        a,b = 0,1
        for _ in range(int(arg)):
            a,b = b,a+b
        return a 

    def main():

        qstat_data = qstat.Qstat()

        q = qsub.Qsub(job,1e9)

        q.push()
        q.pull()

        max_time = 30
        start_time = time.time()

        while not q.complete:
            time.sleep(1)
            if time.time()-start_time >= max_time:
                q.quit()
                print("Job exceeded max time, job terminated.")
                break

        found = False
        for n in qstat_data.process_simple_qstat():
            if n.job_id == q.job_id:
                print("Job still in queue")
                found = True

        if not found:
            print("Job is not in the queue")
        
    if __name__ == "__main__":
        main()

This is equivalent as to using the create_timer functionality:

.. code-block:: python

    from clusterweb.pbs import qsub
    from clusterweb.pbs import qstat

    import time

    def job(arg):
        a,b = 0,1
        for _ in range(int(arg)):
            a,b = b,a+b
        return a 

    def main():

        qstat_data = qstat.Qstat()

        q = qsub.Qsub(job,1e9)

        q.create_timer(30)

        q.push()
        q.pull()

        while not q.complete:
            time.sleep(1)

        print(q.result)

        found = False
        for n in qstat_data.process_simple_qstat():
            if n.job_id == q.job_id:
                print("Job still in queue")
                found = True
                
        if not found:
            print("Job is not in the queue")
        
    if __name__ == "__main__":
        main()















