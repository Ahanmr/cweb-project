import time
import math

from clusterweb.pbs import qsub

test_arg = 5

def job(arg):
	a,b = 1,1
	for _ in range(int(arg)):
		a,b = b,a+b
	return a 

def main():
    q1 = qsub.Qsub(job,test_arg)

    # q1.push()

    # q1.pull()

    # q2 = qsub.Qsub(job,test_arg)

    # q2.push()

    # q2.pull()

    # print("q1 > q2:  {}".format(q1 > q2))
    # print("q1 >= q2: {}".format(q1 >= q2))
    # print("q1 < q2:  {}".format(q1 < q2))
    # print("q1 <= q2: {}".format(q1 <= q2))
    # print("q1 == q2: {}".format(q1 == q2))
    # print("q1 != q2: {}".format(q1 != q2))

    sess = q1 * 5

    sess.push()
    sess.pull()

    while not sess.all_complete:
        time.sleep(1)
        print("Waiting...")

    print(sess.results)

if __name__ == "__main__":
	main()