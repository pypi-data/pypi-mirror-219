import os

from setuptools import find_packages, setup

install_requires = [
	"pip>=21",
	"python-arango>=6.0.0"
]

setup(
	name='aql-builder',
	version=__import__('aql_builder').__version__,
	python_requires='>=3.7',
	url='https://foss.heptapod.net/aquapenguin/aql-builder',
	maintainer='Aqua Penguin',
	maintainer_email='aqua.penguin.34@gmail.com',
	description='ArangoDB AQL builder',
	long_description=open('README.md', encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	packages=find_packages(include=('aql_builder',)),
	install_requires=install_requires,
	classifiers=[
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',
	],
	project_urls={
		'Source': 'https://foss.heptapod.net/aquapenguin/aql-builder',
		'Tracker': 'https://foss.heptapod.net/aquapenguin/aql-builder/-/issues',
	},
)
