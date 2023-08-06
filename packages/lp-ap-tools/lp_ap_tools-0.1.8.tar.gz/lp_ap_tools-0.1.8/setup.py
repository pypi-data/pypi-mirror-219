from setuptools import find_packages, setup

setup(
    name='lp_ap_tools',
    packages=find_packages(),
    version='0.1.8',
    description='A python decorator for creating ActionProvider RO-crates within a Globus flow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Augustus Ellerm',
    license='MIT',
    install_requires=['rocrate', 
                      'pydantic',
                      'flask==2.1.3'],
    setup_requires=['pytest-runner'],
    test_requires=['pytest==4.4.1'],
    test_suite='tests',
    url='https://github.com/GusEllerm/lp_tools.git',
    classifiers=("Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent")
)