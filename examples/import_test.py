import cloudpickle

def wrapper(fnc):
	return cloudpickle.dumps(fnc)