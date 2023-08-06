# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="massivetoollib",
    version="0.0.2",
    description="A pip generic developer package",
    license="MIT",
    author="AngeloChDev",
    author_email="angeloch.dev@gmail.com",
    url="https://github.com/AngeloChDev",
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
         'requests>=2.25.0',
      'fastecdsa>=2.2.1;platform_system!="Windows"',
      'ecdsa>=0.17;platform_system=="Windows"',
      'SQLAlchemy>=1.4.28',
      'numpy==1.19.5;python_version<"3.8"',
      'numpy>=1.21.0;python_version>="3.8"',
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=["Generic Developer Tools"," Wedapp developer"," Offline Software developer","Python package"]
)
