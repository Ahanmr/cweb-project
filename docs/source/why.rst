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

+--------------------------------------------------+-----------------------------------------------+
| Previous Development Process                     | New Development Process                       |
+==================================================+===============================================+
| Write code on local machine with text editor.    | Write code on local machine with text editor. |
+--------------------------------------------------+-----------------------------------------------+
| Copy code over to the cluster or update repo.    | Run code locally.                             |
+--------------------------------------------------+-----------------------------------------------+
| Write PBS Scipt                                  | Recieve output within script.                 |
+--------------------------------------------------+-----------------------------------------------+
| Run ``qsub qsub_script``.                        | Edit code and return to step 2.               |
+--------------------------------------------------+-----------------------------------------------+
| Wait and run ``qstat`` to check for status.      |                                               |
+--------------------------------------------------+-----------------------------------------------+
| Read output in separate files                    |                                               |
+--------------------------------------------------+-----------------------------------------------+
| Edit on the cluster or on local text editor.     |                                               |
+--------------------------------------------------+-----------------------------------------------+
| If edited locally, update code on the cluster.   |                                               |
+--------------------------------------------------+-----------------------------------------------+
| Repeat from step 4.                              |                                               |
+--------------------------------------------------+-----------------------------------------------+

Supports Multiple Types of Devices
##################################



Complete Control Over Distributed Systems
#########################################

Makes It Easy to Create Complex Systems
#######################################
