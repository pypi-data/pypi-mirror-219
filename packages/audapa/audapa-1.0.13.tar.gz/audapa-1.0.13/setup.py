
#if there is the problem like in info.md with python10:
# now: rpm modified pyaudio is at releases at my pyaudioo project. deb and appimage are ok
#
# for pypi and source:
#	apt download audapa
#	sudo dpkg --ignore-depends=python3-pyaudio -i audapa.......deb
#but then, to not see broken count now and then, must remove python3-pyaudio at audapa package dependencies from /var/lib/dpkg/status
#A SOLUTION: overwrite ./build/lib.linux-x86_64-3.10/_portaudio.cpython-310-x86_64-linux-gnu.so at python3-pyaudio equivalent

#pip install --user .
#pip uninstall audapa

pkname='audapa'

import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "info.md").read_text()
ver=(HERE / "v2").read_text()

#import subprocess
#import setuptools.command.build_py
#class BuildPyCommand(setuptools.command.build_py.build_py):
#  """Custom build command."""
#  def run(self):
#    subprocess.run(['touch','qwerty.so'])
#    subprocess.run(['mv','qwerty.so','audapa'])
#    #MANIFEST.in include audapa/qwerty.so
#    #and include_package_data=True
#    setuptools.command.build_py.build_py.run(self)

from setuptools import setup
setup(name=pkname,
	version=ver,
	packages=[pkname],
	#optionals
	#cmdclass={
	#	'build_py': BuildPyCommand
	#},
	#include_package_data=True,
	python_requires='>=3.8',
	install_requires=[
		"pycairo>=1.20.0","PyGObject>=3.40",
		"appdirs>=1.4.3",
		"PyAudio>=0.2.11"],
	description='Audio wave file manipulator',
	long_description=README,
	long_description_content_type="text/markdown",
	url='https://github.com/colin-i/audapa',
	author='colin-i',
	author_email='costin.botescu@gmail.com',
	license='MIT',
	entry_points = {
		'console_scripts': [pkname+'='+pkname+'.main:main']
	}
)
