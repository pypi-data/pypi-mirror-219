from setuptools import setup

import platform

# Check the current operating system
current_os = platform.system()

# Define the supported operating systems
supported_os = ['Windows']

# Verify if the current OS is supported
if current_os not in supported_os:
    raise OSError(f"Unsupported operating system: {current_os}")


setup(
    name='testlibraryorsomething',
    version='1.0.1',
    description='Test Library or Something',
    author='Bamboooz',
    author_email='bambusixmc@gmail.com',
    packages=['testlibraryorsomething'],
    entry_points={
        'console_scripts': [
            'testlibraryorsomething = testlibraryorsomething.__init__:main'
        ]
    },
)
