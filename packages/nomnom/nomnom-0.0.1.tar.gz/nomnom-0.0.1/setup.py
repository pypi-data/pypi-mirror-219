### setup.py for nomnom

from setuptools import setup, find_packages, Extension
import numpy, sys
import re

# auto-updating version code stolen from RadVel (via orbitize!)
def get_property(prop, project):
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open("__init__.py").read(),
    )
    return result.group(1)


def get_requires():
    reqs = []
    for line in open("requirements.txt", "r").readlines():
        reqs.append(line)
    return reqs


setup(
    name="nomnom",
    version=get_property("__version__", "nomnom"),
    description="nomnom turns GW events into 3D visuals",
    url="https://github.com/vikrammanikantan/nomnom",
    author="Jessica Klusmeyer, Bill Smith, Vikram Manikantan",
    author_email="nomnom@gmail.com",
    license="BSD",
    packages=find_packages(),
    package_data={"": ["kernels/*.cu"]},
    ext_modules=None,
    include_dirs=[numpy.get_include()],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="Gravitational Wave Galaxy",
    install_requires=get_requires(),
)
