from setuptools import setup
from src import __version__

try:
	from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

	class bdist_wheel(_bdist_wheel):
		def finalize_options(self):
			_bdist_wheel.finalize_options(self)
			self.root_is_pure = False
except ImportError:
	bdist_wheel = None  # type: ignore

with open("README.md", "r") as fh:
	long_description = fh.read()

with open("requirements.txt") as rq:
	required = rq.read().splitlines()

setup(
	name="weelib",
	version=__version__,
	author="Patrik Katrenak",
	author_email="patrik@katryapps.com",
	description="Additional functions for weepy framework.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/katry/weelib",

	package_dir={"weelib": "src"},
	install_requires=required,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent",
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries",
		"Natural Language :: English",
	],
	# cmdclass={"bdist_wheel": bdist_wheel},
	platforms=["any"],
	python_requires=">=3.10",
)
