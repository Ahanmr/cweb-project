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