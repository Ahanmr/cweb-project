import shutil
import sys
import os 

for (root,dirs,files) in os.walk(os.path.abspath('.'),topdown=True): 
	
	for d in dirs:
		path = os.path.join(root,d)
		if '__pycache__' in path:
			shutil.rmtree(path)

	for f in files:
		path = os.path.join(root,f)
		if '.DS_Store' in path:
			os.remove(path)
