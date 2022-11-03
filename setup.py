
# Thanks to Kenneth Reitz for the sample setup.py
# on which this is based, with a few tweaks
# https://github.com/kennethreitz/setup.py/blob/master/setup.py

from setuptools import setup, find_packages, Command
from shutil import rmtree
import os
import sys

# Package meta-data.
NAME = 'simpleschema'
DESCRIPTION = 'A minimal schema validator'
URL = 'https://github.com/Lrizika/simpleschema'
EMAIL = 'lrizika.simpleschema@lrizika.com'
VERSION = None
LICENSE = 'MIT'
AUTHOR = 'Lrizika'
USE_TEST_PYPI = False
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
PYTHON_VERSION_REQUIRED = '>=3.8.0'

with open("README.md", 'r') as f:
	LONG_DESCRIPTION = f.read()

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
	project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
	with open(os.path.join(here, project_slug, '__version__.py')) as f:
		exec(f.read(), about)
else:
	about['__version__'] = VERSION


class UploadCommand(Command):
	"""Support setup.py upload."""

	description = 'Build and publish the package.'
	user_options = []

	@staticmethod
	def status(s):
		"""Prints things in bold."""
		print('\033[1m{0}\033[0m'.format(s))

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		try:
			self.status('Removing previous builds…')
			rmtree(os.path.join(here, 'dist'))
		except OSError:
			pass

		self.status('Building Source and Wheel (universal) distribution…')
		os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

		if USE_TEST_PYPI:
			self.status('Uploading the package to Test PyPI via Twine…')
			os.system('twine upload --repository testpypi dist/*')
		else:
			self.status('Uploading the package to PyPI via Twine…')
			os.system('twine upload dist/*')

		self.status('Pushing git tags…')
		os.system('git tag v{0}'.format(about['__version__']))
		os.system('git push --tags')

		sys.exit()


setup(
	name=NAME,
	version=about['__version__'],
	license=LICENSE,
	long_description=LONG_DESCRIPTION,
	description=DESCRIPTION,
	author=AUTHOR,
	author_email=EMAIL,
	url=URL,
	long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
	packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
	python_requires=PYTHON_VERSION_REQUIRED,
)
