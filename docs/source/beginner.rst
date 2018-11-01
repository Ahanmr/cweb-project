Beginner Usage Tutorials
========================

Submitting a Single Job with Qsub
---------------------------------

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

.. note:: This is equivalent as to using the create_timer functionality:

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

        q.create_timer(20)

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















