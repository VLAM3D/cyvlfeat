# Fork of cyvlfeat with modified setup.py to create a standalone platform wheel file

When using conda is not possible, platform specific whl files are the next best thing.

However, you'll need to use conda to build the whl.

This fork uses the menpo channel vlfeat package, this repo is a parasitic modification to leverage work of others.
Thanks to cyvlfeat [contributors](https://github.com/menpo/cyvlfeat/graphs/contributors) for maintaining the conda recipes, setuptools scripts and Cython bindings for vlfeat.

## How to build

~~~~
git clone https://github.com/VLAM3D/cyvlfeat.git
cd cylvfeat
git checkout linux_fix
conda create -n buildcyvlfeat python=x.y numpy Cython
activate buildcyvlfeat
conda install -c menpo vlfeat
python setup.py bdist_wheel
~~~~

### Getting the right version number

Necessary steps to get the good version number in the package name:
- Merge the upstream changes from https://github.com/menpo/cyvlfeat
- Commit
- Tag the version (add a 4th version number ex: 0.5.1.1)
- Run `python setup.py bdist_wheel`

## How to tests

Again with conda, but you should test in your target environment for doing all this.

~~~~
conda -n create clean python=x.y numpy
pip install the_whl_you_just_created
python
>>> import cyvlfeat
~~~~

## Back to origin

Go to the original [README](https://github.com/menpo/cyvlfeat/blob/master/README.md)


