from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils.extension import Extension
import setuptools
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

extensions = [
    setuptools.Extension('tsp_spanning.tsp_wrap',
              sources=["tsp_spanning/tsp_wrap.pyx", "tsp_spanning/tsp_cpp.cpp"],
              include_dirs = [np.get_include()] + [os.path.join(current_dir, "tsp_spanning")],
              language='c++', extra_compile_args=["-std=c++11"]),
               #  extra_compile_args=["-std=c++11", "-g", "-DDEBUG"], extra_link_args=["-g"]),
    ]
extensions[0].cython_directives = {"embedsignature": True}

def readme():
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.rst')) as f:
        return f.read()


setuptools.setup(
  version="0.2",
  name = 'tsp_spanning',
  author="Grzegorz Bokota",
  author_email="g.bokota@cent.uw.edu.pl",
  packages=setuptools.find_packages(),
  install_requires=['numpy', 'cython'],
  ext_modules = extensions,
  long_description=readme(),
  long_description_content_type='text/x-rst',
  url='https://github.com/Czaki/tsp_spanning',
  cmdclass={'build_ext': build_ext},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    "Operating System :: OS Independent",
    "Programming Language :: C++",
    "Programming Language :: Python :: Implementation :: CPython",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ]
)