import time
import math

from clusterweb.pbs import qsub

test_arg = 1e5

def job(arg):
	a,b = 1,1
	for _ in range(int(arg)):
		a,b = b,a+b
	return a 

def main():
    q1 = qsub.Qsub(job,5)

    q1.push()

    q1.pull()

    q2 = qsub.Qsub(job,5)

    q2.push()

    q2.pull()

    while not q1.complete and q2.complete:
        time.sleep(1)
        print("Waiting...")

    print(q1.result)

if __name__ == "__main__":
	main()