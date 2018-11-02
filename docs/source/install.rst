Installation
============

Install with Pip
----------------

Pip is the package management system for Python, this is the recommend installation method.

>>> pip install clusterweb

If you don't have root access to the required files pip uses to install a package, such as if you are a non-admin user on a cluster,
use the --user flag.

>>> pip install --user clusterweb

Install with Conda
------------------

.. sidebar:: `Optional` Set up conda environment 

   To keep your libraries across your system clean and unmodified from this isntallation, it is highly recommend that you create a conda environment.

	Create environment:

	>>> conda create -n <ENV_NAME> python=3

	Access environment:

	>>> source activate <ENV_NAME>

Conda is another package management system, but also includes environment control and is the preferred method for when dealing with conda environments.

>>> conda install clusterweb

Install from Source
-------------------

>>> git clone https://github.com/gndctrl2mjrtm/cweb-project.git

>>> cd cweb-project

>>> pip install -r requirements.txt

>>> pip install -e .
