Why Use ClusterWeb
==================

Greater Functionality
#####################

Having all aspects of job submission and monitoring job status be within Python allows for controlling remote jobs through scripting. Instead of having to manually submit each job and manipulate file outputs, the user can control the entire workflow from within the script, have multiple job submissions return their value asynchronous, and create large systems with easy-to-use APIs.

More Cluster Security
#####################

Now that the users can submit jobs locally, it reduces the amount of time that the users spend on the actual cluster and can result in fewer mistakes that may damage the system and mispractice.


Faster Development Time
#######################

ClusterWeb significantly reduces the amount of work required to develop solutions using the DevCloud by creating a simpler development process.

Previous Development Process
----------------------------
Write code on local machine with text editor.
Copy code over to DevCloud or update repo.
Write PBS Scipt for example script.py in qsub_script:

.. code-block:: bash

	#PBS -l nodes=1
	     cd $PBS_O_WORKDIR
	     python script.py

Run ``qsub qsub_script``.
Wait and run ``qstat`` to check for status.
Read output in example 123456.o123456 and 123456.e123456.
In case of errors, either edit on DevCloud or on local text editor.
If edited locally, update code on DevCloud.
Repeat from step 4.

New Development Process
-----------------------
Write code on local machine with text editor.
Run code locally.
Recieve output within script.
Edit code and return to step 2.

Supports Multiple Types of Devices
##################################



Complete Control Over Distributed Systems
#########################################

Makes It Easy to Create Complex Systems
#######################################
