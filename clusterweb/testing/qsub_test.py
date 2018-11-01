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