import time
import math

from cweb.pbs import qsub

test_arg = 1e5

def job(arg):
	a,b = 1,1
	for _ in range(int(arg)):
		a,b = b,a+b
	return a 

def main():
    q = qsub.Qsub(job,5)

    q.push()

    q.pull()

    while not q.complete:
        time.sleep(1)
        print("Waiting...")

    print(q.result)

if __name__ == "__main__":
	main()