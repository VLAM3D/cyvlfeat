from __future__ import print_function
from setuptools import setup, find_packages, Extension
import pkg_resources
from Cython.Build import cythonize
import os.path as op
import sys
import os
import platform
import fnmatch
import versioneer
from shutil import copyfile
from distutils.sysconfig import get_python_inc

<<<<<<< HEAD
INCLUDE_DIRS = [pkg_resources.resource_filename('numpy', 'core/include'), 
                os.path.join(os.path.dirname(sys.executable),'Library','include'),
                os.path.join(get_python_inc(),'..')]
=======
INCLUDE_DIRS = [pkg_resources.resource_filename('numpy', 'core/include'),
                os.path.join(os.path.dirname(sys.executable),'Library','include')]
>>>>>>> build_wheel
LIBRARY_DIRS = [os.path.join(os.path.dirname(sys.executable),'Library','bin')]

print(INCLUDE_DIRS)

SYS_PLATFORM = platform.system().lower()
IS_WIN = platform.system() == 'Windows'
IS_LINUX = 'linux' in SYS_PLATFORM
IS_OSX = 'darwin' == SYS_PLATFORM
IS_UNIX = IS_LINUX or IS_OSX
IS_CONDA = os.environ.get('CONDA_BUILD', False)

def check_copy(src, dst):
    if not os.path.exists(src):
        raise RuntimeError('%s not found' % src)
    print('Copying %s to %s' % (src,dst))
    copyfile(src, dst)

def walk_for_package_data(ext_pattern):
    paths = []
    for root, dirnames, filenames in os.walk('cyvlfeat'):
        for filename in fnmatch.filter(filenames, ext_pattern):
            # Slice cyvlfeat off the beginning of the path
            paths.append(
                op.relpath(os.path.join(root, filename), 'cyvlfeat'))
    return paths


def gen_extension(path_name, sources):
    kwargs = {
        'sources': sources,
        'include_dirs': INCLUDE_DIRS,
        'library_dirs': LIBRARY_DIRS,
        'libraries': ['vl'],
        'language': 'c'
    }
    if IS_UNIX:
        kwargs['extra_compile_args'] = ['-Wno-unused-function', '-Wno-strict-prototypes']
    if IS_LINUX:
        # Add shared lib relative path to RPATH so that every modules find the packaged libvl.so
        kwargs['extra_link_args'] = [ "-Wl,-rpath,${ORIGIN}:${ORIGIN}/.." ]
    return Extension(path_name, **kwargs)


# If we are building from the conda folder,
# then we know we can manually copy some files around
# because we have control of the setup. If you are
# building this manually or pip installing, you must satisfy
# that the vlfeat vl folder is on the PATH (for the headers)
# and that the vl.dll file is visible to the build system
# as well.
if IS_WIN:
    vl_dll_path = os.path.join(os.path.dirname(sys.executable),'Library','bin', 'vl.dll')
    check_copy(vl_dll_path, 'cyvlfeat/vl.dll')
    # sync with the list just below
    cythonized_folders = ['sift', 'fisher', 'hog', 'kmeans', 'generic', 'gmm']
    for f in cythonized_folders:
        check_copy(vl_dll_path, os.path.join('cyvlfeat', f, 'vl.dll'))
elif IS_LINUX:
    vl_so_path = os.path.join(os.path.dirname(sys.executable),'..','lib', 'libvl.so')
    print(vl_so_path)
    check_copy(vl_so_path, 'cyvlfeat/libvl.so')

vl_extensions = [
    gen_extension('cyvlfeat.sift.cysift',
                  [op.join('cyvlfeat', 'sift', 'cysift.pyx')]),
    gen_extension('cyvlfeat.fisher.cyfisher',
                  [op.join('cyvlfeat', 'fisher', 'cyfisher.pyx')]),
    gen_extension('cyvlfeat.hog.cyhog',
                  [op.join('cyvlfeat', 'hog', 'cyhog.pyx')]),
    gen_extension('cyvlfeat.kmeans.cykmeans',
                  [op.join('cyvlfeat', 'kmeans', 'cykmeans.pyx')]),
    gen_extension('cyvlfeat.generic.generic',
                  [op.join('cyvlfeat', 'generic', 'generic.pyx')]),
    gen_extension('cyvlfeat.gmm.cygmm',
                  [op.join('cyvlfeat', 'gmm', 'cygmm.pyx')])
]



# Grab all the pyx and pxd Cython files for uploading to pypi
cython_files = walk_for_package_data('*.[dp][xyl][xdl]')
cython_files += walk_for_package_data('*.so')

setup(
    name='cyvlfeat',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Cython wrapper of the VLFeat toolkit',
    url='https://github.com/menpo/cyvlfeat',
    author='Patrick Snape',
    author_email='p.snape@imperial.ac.uk',
    ext_modules=cythonize(vl_extensions),
    packages=find_packages(),
    package_data={'cyvlfeat': cython_files}
)