from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='Strings-OC',
	version='1.0.1',
	description='Generic functions for dealing with and generating strings',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/strings/',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/strings/',
		'Source': 'https://github.com/ouroboroscoding/strings-python',
		'Tracker': 'https://github.com/ouroboroscoding/strings-python/issues'
	},
	keywords=['strings', 'string manipulation', 'string generation'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['strings'],
	python_requires='>=3.10',
	zip_safe=True
)