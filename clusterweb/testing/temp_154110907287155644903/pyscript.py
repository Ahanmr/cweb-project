
import subprocess

PYTHON_VERSION = 3

script = '''
import pickle
import shutil
import sys
import os

temp_dir = 'temp_154110907287155644903'

try:
    with open(os.path.join(temp_dir,'fnc.pkl'),'rb') as f:
        fnc = pickle.loads(f.read())

    with open(os.path.join(temp_dir,'args.pkl'),'rb') as f:
        args = pickle.loads(f.read())
        
    output = fnc(args)
except Exception as e:
    output = e

with open(os.path.join(temp_dir,'result.pkl'),'wb') as f:
    output = fnc(args)
    f.write(pickle.dumps(fnc(args)))
'''
if PYTHON_VERSION == 2:
    subprocess.call(["python2","-c",script])
else:
    subprocess.call(["python3","-c",script])

