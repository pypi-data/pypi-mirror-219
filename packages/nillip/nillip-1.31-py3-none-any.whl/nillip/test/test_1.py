# from nillip import nil 

import os
import pkg_resources
import subprocess

# List of packages in your script
packages = [
    "shutil",
    "numpy",
    "os",
    "glob",
    "natsort",
    "scipy",
    "h5py",
    "matplotlib",
    "pandas",
    "copy",
    "nillip",
    "platform",
    "subprocess",
    "tqdm",
    "datetime",
    "pytz",
    "cv2",
    "pathlib"
]

def get_version(package):
    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        return None

# Get installed packages and versions
installed = {pkg.key: get_version(pkg.key) for pkg in pkg_resources.working_set}

# Filter for only the packages you're interested in
to_install = {pkg: installed[pkg] for pkg in packages if pkg in installed}

# Write to requirements.txt
with open('requirements.txt', 'w') as f:
    for pkg, version in to_install.items():
        f.write(f'{pkg}=={version}\n')
