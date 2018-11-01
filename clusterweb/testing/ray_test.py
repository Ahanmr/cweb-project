import ray
import numpy as np
import time

def test_function(arg):
	time.sleep(1)

@ray.remote
def ray_test_function(arg):
	time.sleep(1)

def main():
	c = 100000


	start_time = time.time()
	output = []
	for _ in range(10):
		output.append(test_function(c))


	print("Time elapsed: {}".format(time.time()-start_time))

	
	ray.init()
	start_time = time.time()
	ray.get([ray_test_function.remote(c) for i in range(10)])
	print("Time elapsed: {}".format(time.time()-start_time))



if __name__ == "__main__":
	main()