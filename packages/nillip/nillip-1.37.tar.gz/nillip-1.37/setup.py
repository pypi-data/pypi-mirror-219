from setuptools import setup
from setuptools import find_packages
import os
from nillip import nil

with open("README.md", "r") as fh:
    long_description = fh.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename[0] != '.':
                paths.append(os.path.join('..', path, filename))
    return paths


include_files = package_files(nil.get_nillip_path()) # need to verify this will work on all machines... using utils
# before nillip is installed??????

remove_list = ['final_model/final_resnet50V2_full_model',
               'nillip_data/training_data',
               'final_model/extra_LGBM_models']
include_files = list(nil.lister_it(include_files, remove_string=remove_list))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='nillip',
      version='1.37',
      author="Phillip Maire",
      license='MIT',
      description='custom utils package for me, but feel free to use it if you want',
      packages=find_packages(),
      author_email='phillip.maire@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="", #"https://github.com/PhillipMaire/nillip",
      zip_safe=False,
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
      python_requires='>=3.6',
      install_requires=requirements,
      package_data={'': include_files},
      include_package_data=True
      )

