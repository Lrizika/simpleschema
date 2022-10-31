from setuptools import setup, find_packages

with open("README.md", 'r') as f:
	long_description = f.read()

setup(
	name='simpleschema',
	version='0.1.1',
	license='MIT',
	long_description=long_description,
	description='A minimal schema validator',
	author='LRizika',
	author_email='lrizika.simpleschema@lrizika.com',
	url='https://github.com/Lrizika/simpleschema',
	packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
)
